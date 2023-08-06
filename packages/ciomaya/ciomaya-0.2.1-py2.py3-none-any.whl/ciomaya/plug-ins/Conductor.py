import sys

# The template mut be imported before the plugin node.
import maya.api.OpenMaya as om
from ciocore import data as coredata
from ciomaya.lib.ae import AEconductorRenderTemplate
from ciomaya.lib import conductor_menu
from ciomaya.lib.nodes.conductorRender import conductorRender


def maya_useNewAPI():
    pass


def initializePlugin(obj):
    # Use "0.2.1 to cause the version to be replaced at build time."
    plugin = om.MFnPlugin(obj, "Conductor", "0.2.1", "Any")
    try:
        plugin.registerNode(
            "conductorRender",
            conductorRender.id,
            conductorRender.creator,
            conductorRender.initialize,
            om.MPxNode.kDependNode,
        )
    except:
        sys.stderr.write("Failed to register conductorRender\n")
        raise

    conductor_menu.load()
    
    coredata.init(product="maya-io")


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(conductorRender.id)
    except:
        sys.stderr.write("Failed to deregister conductorRender\n")
        raise

    conductor_menu.unload()
