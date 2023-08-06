from phases.util.pdict import pdict
import yaml
import os
import pyPhases
import sys
from ..util.Logger import classLogger


class Misconfigured(Exception):
    pass


@classLogger
class Base(object):
    outputDir = None
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.config = {}
        self.projectFileName = "project.yaml"
        self.projectGridFile = None
        self.projectConfigFileName = None
        self.config = None

    def run(self):
        raise NotImplementedError("You must implement the run() method yourself!")

    def overwriteConfig(self, config, values, path=[]):
        """Recursively overwrite the project config with the values in a diffrent config.

        Args:
            config ([type]): config to overwrite
            values ([type]): overwrite values in a dictionary
            path (list, optional): [description]. Defaults to [].

        Returns:
            dict: overwritten config
        """
        config = pdict(config)
        for field in values:
            value = values[field]
            p = path + [field]

            if isinstance(value, dict):
                c = config.__getitem__(p, create=True)
                config[p] = self.overwriteConfig(c, value, [])
            else:
                config[p] = values[field]

        return config

    def overwriteConfigByEnviroment(self, config, path=[]):
        config = pdict(config)
        for field in config:
            value = config[field]
            p = path + [str(field)]

            if isinstance(value, dict):
                config[field] = self.overwriteConfigByEnviroment(value, p)
            else:
                v = os.environ.get("PHASE_CONFIG_" + "_".join(p))
                if v is not None:
                    self.logDebug("overwrite config %s by env: %s" % (p, v))
                    config[field] = v

        return config

    def prepareConfig(self):
        projectFile = open(self.projectFileName, "r")
        yamlContent = projectFile.read()
        projectConfig = yaml.load(yamlContent, Loader=yaml.SafeLoader)
        projectFile.close()

        if self.projectConfigFileName is not None:
            configFiles = self.projectConfigFileName.split(",")
            for configFile in configFiles:
                self.logDebug("parse user config: %s" % configFile)
                yamlFile = open(configFile, "r")
                yamlContent = yamlFile.read()
                userConfig = yaml.load(yamlContent, Loader=yaml.SafeLoader)
                yamlFile.close()
                startPath = [] if "isFullConfig" in userConfig and userConfig["isFullConfig"] else ["config"]
                projectConfig = self.overwriteConfig(projectConfig, userConfig, startPath)

        projectConfig["config"] = self.overwriteConfigByEnviroment(projectConfig["config"])

        self.validateConfig(projectConfig)
        if self.outputDir == None:
            self.outputDir = projectConfig["name"]
        self.config = projectConfig
        self.normalizeConfigArrays()

        self.preparePhases()
        self.preparePackageConfig()

    def validateConfig(self, config):
        # check required fields
        required = ["name", "namespace", "phases"]
        for field in required:
            if not field in config:
                raise Misconfigured(u"%s is required in the project yaml file" % (field))

        # set default values
        defaultValues = {
            "storage": ["FileStorage"],
            "publisher": [],
            "exporter": ["ObjectExporter"],
            "usedClasses": [],
        }
        # for field in defaultValues:
        for field in defaultValues:
            if not field in config:
                config[field] = defaultValues[field]

    def registerClassName(self, classObj, package):
        className = classObj["name"]
        ucFirstClassname = className[0].upper() + className[1:]
        userClassName = "user" + ucFirstClassname
        systemClassName = "system" + ucFirstClassname

        self.config[userClassName] = []
        self.config[systemClassName] = []

        systemclass = self.checkIfClassExistsInPyPhases(className, package)
        if systemclass:
            packagePre = "pyPhases."
        else:
            packagePre = ""

        classObj["package"] = packagePre + package
        classObj["packageName"] = package
        classObj["system"] = systemclass

        if systemclass:
            self.config[systemClassName].append(classObj)
        else:
            self.config[userClassName].append(classObj)
        self.config["usedClasses"].append(classObj)
        return classObj

    def preparePackageConfig(self):
        self.config["packages"] = []
        packages = {}
        for classObj in self.config["usedClasses"]:
            if not classObj["system"]:
                if classObj["packageName"] in packages:
                    packages[classObj["packageName"]]["imports"].append(classObj["name"])
                else:
                    packages[classObj["packageName"]] = {"name": classObj["packageName"], "imports": [classObj["name"]]}
        for name in packages:
            self.config["packages"].append(packages[name])

    def preparePhases(self):
        # flatten phases and extract stages
        self.config["stages"] = []
        self.config["userPhases"] = []
        self.config["phaseClasses"] = []
        lastPhase = None
        for stageOrPhase in self.config["phases"]:
            isPhase = type(stageOrPhase) == dict
            if isPhase:
                stageName = "default"
                phases = [stageOrPhase]
            else:
                stageName = stageOrPhase
                phases = self.config["stages"]["phases"]

            if stageName not in self.config["stages"]:
                self.config["stages"].append(stageName)

            for phase in phases:
                phase["stage"] = stageName
                self.config["userPhases"].append(phase)
                self.registerClassName(phase, "phases")
                if lastPhase != None:
                    lastPhase["next"] = phase
                lastPhase = phase

        self.config["phases"] = self.config["userPhases"]

    def normalizeDataArray(self, objectOrString):
        if isinstance(objectOrString, str):
            return {"name": objectOrString, "description": ""}

        if not "name" in objectOrString:
            raise Exception("One Object does not have a name")

        if "config" in objectOrString:
            objectOrString["config"]["items"] = self.normalizeDict(objectOrString["config"])

        return objectOrString

    def normalizeDict(self, dictObj):
        arrayForTemplate = []

        for (__, name) in enumerate(dictObj):
            arrayForTemplate.append({"name": name, "value": dictObj[name]})
        return arrayForTemplate

    def normalizeConfigArrays(self):
        arrayFields = ["publisher", "storage", "exporter", "data"]
        for field in arrayFields:
            if field not in self.config:
                self.config[field] = []
            for index, arrayOrString in enumerate(self.config[field]):
                obj = self.normalizeDataArray(arrayOrString)
                obj = self.registerClassName(obj, field)
                self.config[field][index] = obj

    def getPackagePath(self, path):
        d = os.path.dirname(sys.modules["phases"].__file__)
        return os.path.join(d, path)

    def checkIfClassExistsInPyPhases(self, className, package):
        try:
            module = getattr(pyPhases, package)
            getattr(module, className)
            return True
        except AttributeError:
            pass

        return False
