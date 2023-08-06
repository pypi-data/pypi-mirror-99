from .onmanager import ONProcess
from xml.etree import ElementTree

namespace = ""


class OneNote:

    def __init__(self):
        self.process = ONProcess()
        global namespace
        namespace = self.process.namespace
        self.xml = self.process.get_hierarchy("", 4)
        self.object_tree = ElementTree.fromstring(self.xml)
        self.hierarchy = Hierarchy(self.object_tree)

    def get_page_content(self, page_id):
        page_content_xml = ElementTree.fromstring(self.process.get_page_content(page_id))
        return PageContent(page_content_xml)
        # return page_content_xml

    def names(self):
        """所有笔记本的名称"""
        ls = list(map(lambda x: x.name, self.hierarchy))
        return ls

    def nicknames(self):
        """所有笔记本的昵称"""
        ls = list(map(lambda x: x.nickname, self.hierarchy))
        return ls

    def __getitem__(self, item):
        """通过编号或名称索引获得笔记本"""
        return self.hierarchy[item]


class Hierarchy:

    def __init__(self, xml=None):
        self.xml = xml
        self._children = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __deserialize_from_xml(self, xml):
        self._children = [Notebook(n) for n in xml]

    def __iter__(self):
        for c in self._children:
            yield c

    def __getitem__(self, item):
        """通过编号或名称索引子节点内容"""
        if isinstance(item, int):
            return self._children[item]
        elif isinstance(item, str):
            for nb in self:
                if nb.nickname == item:
                    return nb
        return None


class HierarchyNode:

    def __init__(self, parent=None):
        self.name = ""
        self.path = ""
        self.id = ""
        self.last_modified_time = ""
        self.synchronized = ""

    def deserialize_from_xml(self, xml):
        self.name = xml.get("name")
        self.path = xml.get("path")
        self.id = xml.get("ID")
        self.last_modified_time = xml.get("lastModifiedTime")


class Notebook(HierarchyNode):

    def __init__(self, xml=None):
        self.xml = xml
        super().__init__(self)
        self.nickname = ""
        self.color = ""
        self.is_currently_viewed = ""
        self.recycleBin = None
        self._children = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __deserialize_from_xml(self, xml):
        HierarchyNode.deserialize_from_xml(self, xml)
        self.nickname = xml.get("nickname")
        self.color = xml.get("color")
        self.is_currently_viewed = xml.get("isCurrentlyViewed")
        self.recycleBin = None
        for node in xml:
            if node.tag == namespace + "Section":
                self._children.append(Section(node, self))

            elif node.tag == namespace + "SectionGroup":
                if node.get("isRecycleBin"):
                    self.recycleBin = SectionGroup(node, self)
                else:
                    self._children.append(SectionGroup(node, self))

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        """通过编号或名称索引子节点内容"""
        if isinstance(item, int):
            return self._children[item]
        elif isinstance(item, str):
            for nb in self:
                if nb.name == item:
                    return nb
        return None


class SectionGroup(HierarchyNode):

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        super().__init__(self)
        self.is_recycle_Bin = False
        self._children = []
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return self.name

    def __deserialize_from_xml(self, xml):
        HierarchyNode.deserialize_from_xml(self, xml)
        self.is_recycle_Bin = xml.get("isRecycleBin")
        for node in xml:
            if node.tag == namespace + "SectionGroup":
                self._children.append(SectionGroup(node, self))
            if node.tag == namespace + "Section":
                self._children.append(Section(node, self))

    def __getitem__(self, item):
        """通过编号或名称索引子节点内容"""
        if isinstance(item, int):
            return self._children[item]
        elif isinstance(item, str):
            for nb in self:
                if nb.name == item:
                    return nb
        return None


class Section(HierarchyNode):

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        super().__init__(self)
        self.color = ""
        self.read_only = False
        self.is_currently_viewed = False
        self._children = []
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return self.name

    def __deserialize_from_xml(self, xml):
        HierarchyNode.deserialize_from_xml(self, xml)
        self.color = xml.get("color")
        try:
            self.read_only = xml.get("readOnly")
        except Exception as e:
            self.read_only = False
        try:
            self.is_currently_viewed = xml.get("isCurrentlyViewed")
        except Exception as e:
            self.is_currently_viewed = False

        self._children = [Page(node, self) for node in xml]

    def __getitem__(self, item):
        """通过编号或名称索引子节点内容"""
        if isinstance(item, int):
            return self._children[item]
        elif isinstance(item, str):
            for nb in self:
                if nb.name == item:
                    return nb
        return None


class Page:

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.name = ""
        self.id = ""
        self.date_time = ""
        self.last_modified_time = ""
        self.page_level = ""
        self.is_currently_viewed = ""
        self._children = []
        self.parent = parent_node
        if xml is not None:  # != None is required here, since this can return false
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return self.name

        # Get / Set Meta

    def __deserialize_from_xml(self, xml):
        self.xml = xml
        self.name = xml.get("name")
        self.id = xml.get("ID")
        self.date_time = xml.get("dateTime")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.page_level = xml.get("pageLevel")
        self.is_currently_viewed = xml.get("isCurrentlyViewed")
        self._children = [Meta(node) for node in xml]

    def getxml(self):
        """获得页面的"""
        return ONProcess().get_page_content(self.id)


class Meta:

    def __init__(self, xml=None):
        self.xml = xml
        self.name = ""
        self.content = ""
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __str__(self):
        return self.name

    def __deserialize_from_xml(self, xml):
        self.name = xml.get("name")
        self.id = xml.get("content")

    def getxml(self):
        """获得页面的"""
        return ONProcess().get_page_content(self.id)


class PageContent:

    def __init__(self, xml=None):
        self.xml = xml
        self.name = ""
        self.id = ""
        self.date_time = ""
        self.last_modified_time = ""
        self.page_level = ""
        self.lang = ""
        self.is_currently_viewed = ""
        self._children = []
        self.files = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return self.name

    def __deserialize_from_xml(self, xml):
        self.name = xml.get("name")
        self.id = xml.get("ID")
        self.date_time = xml.get("dateTime")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.page_level = xml.get("pageLevel")
        self.lang = xml.get("lang")
        self.is_currently_viewed = xml.get("isCurrentlyViewed")
        for node in xml:
            if node.tag == namespace + "Outline":
                self._children.append(Outline(node))
            elif node.tag == namespace + "Ink":
                self.files.append(Ink(node))
            elif node.tag == namespace + "Image":
                self.files.append(Image(node))
            elif node.tag == namespace + "InsertedFile":
                self.files.append(InsertedFile(node))
            elif node.tag == namespace + "Title":
                self._children.append(Title(node))


class Title:

    def __init__(self, xml=None):
        self.xml = xml
        self.style = ""
        self.lang = ""
        self._children = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __str__(self):
        return "Page Title"

    def __iter__(self):
        for c in self._children:
            yield c

    def __deserialize_from_xml(self, xml):
        self.style = xml.get("style")
        self.lang = xml.get("lang")
        for node in xml:
            if node.tag == namespace + "OE":
                self._children.append(OE(node, self))


class Outline:

    def __init__(self, xml=None):
        self.xml = xml
        self.author = ""
        self.author_initials = ""
        self.last_modified_by = ""
        self.last_modified_by_initials = ""
        self.last_modified_time = ""
        self.id = ""
        self._children = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        return "Outline"

    def __deserialize_from_xml(self, xml):
        self.author = xml.get("author")
        self.author_initials = xml.get("authorInitials")
        self.last_modified_by = xml.get("lastModifiedBy")
        self.last_modified_by_initials = xml.get("lastModifiedByInitials")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.id = xml.get("objectID")
        append = self._children.append
        for node in xml:
            if node.tag == namespace + "OEChildren":
                for childNode in node:
                    if childNode.tag == namespace + "OE":
                        append(OE(childNode, self))


class Position:

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.x = ""
        self.y = ""
        self.z = ""
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __deserialize_from_xml(self, xml):
        self.x = xml.get("x")
        self.y = xml.get("y")
        self.z = xml.get("z")


class Size:

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.width = ""
        self.height = ""
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __deserialize_from_xml(self, xml):
        self.width = xml.get("width")
        self.height = xml.get("height")


class OE:

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.creation_time = ""
        self.last_modified_time = ""
        self.last_modified_by = ""
        self.id = ""
        self.alignment = ""
        self.quick_style_index = ""
        self.style = ""
        self.text = ""
        self._children = []
        self.parent = parent_node
        self.files = []
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        for c in self._children:
            yield c

    def __str__(self):
        try:
            return self.text
        except AttributeError:
            return "Empty OE"

    def __deserialize_from_xml(self, xml):
        self.creation_time = xml.get("creationTime")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.last_modified_by = xml.get("lastModifiedBy")
        self.id = xml.get("objectID")
        self.alignment = xml.get("alignment")
        self.quick_style_index = xml.get("quickStyleIndex")
        self.style = xml.get("style")

        for node in xml:
            if node.tag == namespace + "T":
                if node.text is not None:
                    self.text = node.text
                else:
                    self.text = "NO TEXT"

            elif node.tag == namespace + "OEChildren":
                for childNode in node:
                    if childNode.tag == namespace + "OE":
                        self._children.append(OE(childNode, self))

            elif node.tag == namespace + "Image":
                self.files.append(Image(node, self))

            elif node.tag == namespace + "InkWord":
                self.files.append(Ink(node, self))

            elif node.tag == namespace + "InsertedFile":
                self.files.append(InsertedFile(node, self))


class InsertedFile:

    # need to add position data to this class

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.path_cache = ""
        self.path_source = ""
        self.preferred_name = ""
        self.last_modified_time = ""
        self.last_modified_by = ""
        self.id = ""
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        yield None

    def __str__(self):
        try:
            return self.preferredName
        except AttributeError:
            return "Unnamed File"

    def __deserialize_from_xml(self, xml):
        self.path_cache = xml.get("pathCache")
        self.path_source = xml.get("pathSource")
        self.preferred_name = xml.get("preferredName")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.last_modified_by = xml.get("lastModifiedBy")
        self.id = xml.get("objectID")


class Ink:

    # need to add position data to this class

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.recognized_text = ""
        self.x = ""
        self.y = ""
        self.ink_origin_x = ""
        self.ink_origin_y = ""
        self.width = ""
        self.height = ""
        self.data = ""
        self.callback_id = ""
        self.parent = parent_node

        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        yield None

    def __str__(self):
        try:
            return self.recognizedText
        except AttributeError:
            return "Unrecognized Ink"

    def __deserialize_from_xml(self, xml):
        self.recognized_text = xml.get("recognizedText")
        self.x = xml.get("x")
        self.y = xml.get("y")
        self.ink_origin_x = xml.get("inkOriginX")
        self.ink_origin_y = xml.get("inkOriginY")
        self.width = xml.get("width")
        self.height = xml.get("height")

        for node in xml:
            if node.tag == namespace + "CallbackID":
                self.callback_id = node.get("callbackID")
            elif node.tag == namespace + "Data":
                self.data = node.text


class Image:

    def __init__(self, xml=None, parent_node=None):
        self.xml = xml
        self.format = ""
        self.original_page_number = ""
        self.last_modified_time = ""
        self.id = ""
        self.callback_id = None
        self.data = ""
        self.parent = parent_node
        if xml is not None:
            self.__deserialize_from_xml(xml)

    def __iter__(self):
        yield None

    def __str__(self):
        return self.format + " Image"

    def __deserialize_from_xml(self, xml):
        self.format = xml.get("format")
        self.original_page_number = xml.get("originalPageNumber")
        self.last_modified_time = xml.get("lastModifiedTime")
        self.id = xml.get("objectID")
        for node in xml:
            if node.tag == namespace + "CallbackID":
                self.callback_id = node.get("callbackID")
            elif node.tag == namespace + "Data":
                if node.text is not None:
                    self.data = node.text
