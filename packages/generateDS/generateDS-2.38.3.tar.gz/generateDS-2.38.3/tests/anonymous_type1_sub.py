#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 3.8.8 (default, Feb 24 2021, 21:46:12)  [GCC 7.3.0]
#
# Command line options:
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--no-warnings', '')
#   ('--silence', '')
#   ('--member-specs', 'list')
#   ('-f', '')
#   ('-o', 'tests/anonymous_type2_sup.py')
#   ('-s', 'tests/anonymous_type2_sub.py')
#   ('--super', 'anonymous_type2_sup')
#
# Command line arguments:
#   tests/anonymous_type.xsd
#
# Command line:
#   generateDS.py --no-dates --no-versions --no-warnings --silence --member-specs="list" -f -o "tests/anonymous_type2_sup.py" -s "tests/anonymous_type2_sub.py" --super="anonymous_type2_sup" tests/anonymous_type.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

import os
import sys
from lxml import etree as etree_

import anonymous_type2_sup as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class FooListSub(supermod.FooList):
    def __init__(self, attribute01='0', attribute02='none', Foo=None, Bar=None, Baz=None, **kwargs_):
        super(FooListSub, self).__init__(attribute01, attribute02, Foo, Bar, Baz,  **kwargs_)
supermod.FooList.subclass = FooListSub
# end class FooListSub


class FooTypeSub(supermod.FooType):
    def __init__(self, FooType_member=None, **kwargs_):
        super(FooTypeSub, self).__init__(FooType_member,  **kwargs_)
supermod.FooType.subclass = FooTypeSub
# end class FooTypeSub


class BarTypeSub(supermod.BarType):
    def __init__(self, BarType_member=None, **kwargs_):
        super(BarTypeSub, self).__init__(BarType_member,  **kwargs_)
supermod.BarType.subclass = BarTypeSub
# end class BarTypeSub


class BazTypeSub(supermod.BazType):
    def __init__(self, BazType_member=None, **kwargs_):
        super(BazTypeSub, self).__init__(BazType_member,  **kwargs_)
supermod.BazType.subclass = BazTypeSub
# end class BazTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FooList'
        rootClass = supermod.FooList
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='',
##             pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FooList'
        rootClass = supermod.FooList
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         content = etree_.tostring(
##             rootElement, pretty_print=True,
##             xml_declaration=True, encoding="utf-8")
##         sys.stdout.write(content)
##         sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FooList'
        rootClass = supermod.FooList
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FooList'
        rootClass = supermod.FooList
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
##     if not silence:
##         sys.stdout.write('#from anonymous_type2_sup import *\n\n')
##         sys.stdout.write('import anonymous_type2_sup as model_\n\n')
##         sys.stdout.write('rootObj = model_.rootClass(\n')
##         rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
##         sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
