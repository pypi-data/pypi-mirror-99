from PyQt5.QtCore import  QSettings, QCoreApplication, QTranslator, QObject
from PyQt5.QtGui import QIcon,  QPixmap
from PyQt5.QtWidgets import  QApplication, qApp
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date,  datetime

from caloriestracker.connection_pg import argparse_connection_arguments_group, Connection
from caloriestracker.datetime_functions import  string2date, dtaware_now
from caloriestracker.version import __version__,  __versiondatetime__
from colorama import Fore, Style
from caloriestracker.database_update import database_update
from caloriestracker.libmanagers import ObjectManager
from caloriestracker.objects.activity import ActivityManager
from caloriestracker.objects.company import CompanyAllManager
from caloriestracker.objects.additives import AdditiveManager_all
from caloriestracker.objects.additive_risk import AdditiveRiskManager_all
from caloriestracker.objects.food_type import FoodTypeManager_all
from caloriestracker.objects.product import ProductAllManager
from caloriestracker.objects.productelaborated import ProductElaboratedManager_from_sql
from caloriestracker.objects.user import UserManager_from_db
from caloriestracker.objects.weightwish import WeightWishManager
from caloriestracker.package_resources import package_filename
from signal import signal, SIGINT
from sys import argv, exit
from caloriestracker.translationlanguages import TranslationLanguageManager
from logging import basicConfig, DEBUG, INFO, CRITICAL, ERROR, WARNING, info, debug


class Mem(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.con=None
        self.inittime=datetime.now()
        signal(SIGINT, self.signal_handler)
        self._products_maintainer_mode=False

    def epilog(self):
        return self.tr("If you like this app, please give me a star in GitHub (https://github.com/turulomio/caloriestracker).")+"\n" + self.tr("Developed by Mariano Mu\xf1oz 2019-{} \xa9".format(__versiondatetime__.year))
        
    def load_db_data(self, progress=True):
        """Esto debe ejecutarse una vez establecida la conexión"""
        inicio=datetime.now()

        self.data=DBData(self)
        self.data.load(progress)

        info("Loading db data took {}".format(datetime.now()-inicio))

    def setProductsMaintainerMode(self, boolean):
        self._products_maintainer_mode=boolean
        
    def isProductsMaintainerMode(self):
        return self._products_maintainer_mode

    def __del__(self):
        try:
            self.con.disconnect()
        except:
            pass
            

    ## Sets debug sustem, needs
    def addDebugSystem(self, level):
        logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
        dateFormat='%F %I:%M:%S'

        if level=="DEBUG":#Show detailed information that can help with program diagnosis and troubleshooting. CODE MARKS
            basicConfig(level=DEBUG, format=logFormat, datefmt=dateFormat)
        elif level=="INFO":#Everything is running as expected without any problem. TIME BENCHMARCKS
            basicConfig(level=INFO, format=logFormat, datefmt=dateFormat)
        elif level=="WARNING":#The program continues running, but something unexpected happened, which may lead to some problem down the road. THINGS TO DO
            basicConfig(level=WARNING, format=logFormat, datefmt=dateFormat)
        elif level=="ERROR":#The program fails to perform a certain function due to a bug.  SOMETHING BAD LOGIC
            basicConfig(level=ERROR, format=logFormat, datefmt=dateFormat)
        elif level=="CRITICAL":#The program encounters a serious error and may stop running. ERRORS
            basicConfig(level=CRITICAL, format=logFormat, datefmt=dateFormat)
        info("Debug level set to {}".format(level))
        self.debuglevel=level
        
    ## Adds the commons parameter of the program to argparse
    ## @param parser It's a argparse.ArgumentParser
    def addCommonToArgParse(self, parser):
        parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondatetime__.date()))
        parser.add_argument('--debug', help="Debug program information", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="ERROR")

    def signal_handler(self, signal, frame):
            print(Style.BRIGHT+Fore.RED+"You pressed 'Ctrl+C', exiting...")
            exit(1)
            
    ## To translate hardcoded strings
    def trHS(self, s):
        return qApp.translate("HardcodedStrings", s)

class MemGui(Mem):
    def __init__(self):
        Mem.__init__(self)

    def qicon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/caloriestracker/caloriestracker.png"), QIcon.Normal, QIcon.Off)
        return icon

    ## Returns an icon for admin 
    def qicon_admin(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/caloriestracker/admin.png"), QIcon.Normal, QIcon.Off)
        return icon

class MemInit(MemGui):
    def __init__(self):
        MemGui.__init__(self)
        
        self.settings=QSettings()

    def run(self):
        self.args=self.parse_arguments()
        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        self.app=QApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        self.load_translation()
                
    def load_translation(self):
        self.qtranslator=QTranslator(self.app)
        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value("frmAccess/language", "en"))
        filename=package_filename("caloriestracker", "i18n/caloriestracker_{}.qm".format(self.languages.selected.id))
        self.qtranslator.load(filename)
        info("TranslationLanguage changed to {}".format(self.languages.selected.id))
        self.app.installTranslator(self.qtranslator)

    def parse_arguments(self):
        self.parser=ArgumentParser(prog='caloriestracker_init', description=self.tr('Create a new caloriestracker database'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        argparse_connection_arguments_group(self.parser, default_db="caloriestracker")
        args=self.parser.parse_args()
        return args

class MemConsole(Mem):
    def __init__(self):
        Mem.__init__(self)        
        self.app=QCoreApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        self.settings=QSettings()
        self.localzone=self.settings.value("mem/localzone", "Europe/Madrid")
        self.load_translation()
        self.create_parser()

    ##Must be overriden for other MemScripts
    def run(self, args=None):   
        self.args=self.parser.parse_args(args)
        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        #Changing types of args
        self.args.date=string2date(self.args.date)
        self.args.users_id=int(self.args.users_id)
        if self.args.elaborated!=None:
            self.args.elaborated=int(self.args.elaborated)

        
        self.con=self.connection()
        if self.con.is_active()==False:
            exit(1)
        
        database_update(self.con, "caloriestracker", __versiondatetime__, "Console")
        
        self.load_db_data(False)
        
        self.user=self.data.users.find_by_id(1)
        
                
    def load_translation(self):
        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value("frmAccess/language", "en"))
        self.languages.cambiar(self.languages.selected.id, "caloriestracker")

    def connection(self):
        con=Connection()
        con.user=self.args.user
        con.server=self.args.server
        con.port=self.args.port
        con.db=self.args.db
        con.get_password()
        con.connect()
        return con
        
    ## Must be overriden for other MemScripts
    def create_parser(self):
        self.parser=ArgumentParser(prog='caloriestracker_console', description=self.tr('Report of calories'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        argparse_connection_arguments_group(self.parser, default_db="caloriestracker")
        group = self.parser.add_argument_group("Find parameters")
        group.add_argument('--date', help=self.tr('Date to show'), action="store", default=str(date.today()))
        group.add_argument('--users_id', help=self.tr('User id'), action="store", default=1)
        group.add_argument('--find', help=self.tr('Find data'), action="store", default=None)
        group.add_argument('--add_company', help=self.tr("Adds a company"), action="store_true", default=False)
        group.add_argument('--add_product', help=self.tr("Adds a product"), action="store_true", default=False)
        group.add_argument('--add_meal', help=self.tr("Adds a company"), action="store_true", default=False)
        group.add_argument('--add_biometrics', help=self.tr("Adds biometric information"), action="store_true", default=False)
        group.add_argument('--contribution_dump', help=self.tr("Generate a dump to collaborate updating companies and products"), action="store_true", default=False)
        group.add_argument('--parse_contribution_dump', help=self.tr("Parses a dump and generates sql files for the package and for the dump owner"), action="store", default=None)
        group.add_argument('--update_after_contribution',  help=self.tr("Converts personal data to system data in the database using generated sql file of the dump owner"),  action="store", default=None)
        group.add_argument('--elaborated', help=self.tr("Show elaborated product"), action="store", default=None)


class MemCaloriestracker(MemGui):
    def __init__(self):        
        MemGui.__init__(self)
        self._products_maintainer_mode=False
        self.clipboard=ObjectManager()#Manager to work with copy/paste clipboard
 

    def run(self):
        self.args=self.parse_arguments()
        self.addDebugSystem(self.args.debug)
        self.app=QApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        self.con=None

        self.frmMain=None #Pointer to mainwidget
        self.closing=False#Used to close threads
        self.url_wiki="https://github.com/turulomio/caloriestracker/wiki"
    
    def parse_arguments(self):
        self.parser=ArgumentParser(prog='caloriestracker', description=self.tr('Report of calories'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        self.parser.add_argument('--products_maintainer', help=self.tr("Products mantainer interface (only developers)"), action="store_true", default=False)
        args=self.parser.parse_args()
        return args
        
    def setLocalzone(self):
        self.localzone=self.settings.value("mem/localzone", "Europe/Madrid")

    ## @return dtaware with self.localzone as OFFSEt
    def now(self):
        return dtaware_now(self.localzone)

class MemMaintenanceProductSystem2Personal(MemConsole):
    def __init__(self):
        MemConsole.__init__(self)

    ##Must be overriden for other MemScripts
    def run(self, args=None):   
        self.args=self.parser.parse_args(args)
        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        #Changing types of args
        self.args.system=int(self.args.system)

        self.con=self.connection()
        if self.con.is_active()==False:
            exit(1)
        
        database_update(self.con, "caloriestracker", __versiondatetime__, "Console")
        
        self.load_db_data(False)

        self.user=self.data.users.find_by_id(1)
        
        
    ## Must be overriden for other MemScripts
    def create_parser(self):
        self.parser=ArgumentParser(prog='caloriestracker_maintenance_products_system2personal', description=self.tr('Converts a system product in a personal one'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        argparse_connection_arguments_group(self.parser, default_db="caloriestracker")
        group = self.parser.add_argument_group("Find parameters")
        group.add_argument('--system', help=self.tr('System product'), action="store", required=True)
        
class DBData:
    def __init__(self, mem):
        self.mem=mem

    def load(self, progress=True):
        start=datetime.now()
        
        self.activities=ActivityManager(self.mem)
        self.weightwishes=WeightWishManager(self.mem)
        
        self.companies=CompanyAllManager(self.mem)
        self.companies.load_all()
        
        self.foodtypes=FoodTypeManager_all(self.mem)
        self.additiverisks=AdditiveRiskManager_all(self.mem)
        self.additives=AdditiveManager_all(self.mem)

        self.products=ProductAllManager(self.mem)
        self.products.load_all()
        
        self.elaboratedproducts=ProductElaboratedManager_from_sql(self.mem, "select * from elaboratedproducts order by name")
        
        self.users=UserManager_from_db(self.mem, "select * from users", progress)
        self.mem.user=self.mem.data.users.find_by_id(int(self.mem.settings.value("mem/currentuser", 1)))
        if self.mem.user==None:
            self.mem.user=self.mem.data.users.find_by_id(1)#For empty databases (contribution)     
        self.mem.user.needStatus(1)
        
        debug("DBData took {}".format(datetime.now()-start))
