from lxml import etree

### Tree


def load_tree(file_path):
    tree = etree.parse(file_path)
    return tree


### Children


def get_children(element):
    return list(element)


def get_descendants(element):
    descendants = []
    for child in element.iter():
        descendants.append(child)
    return descendants


### Element


def get_tree_root(tree):
    root = tree.getroot()
    return root


def get_source_file_name(element):
    return element.base


def get_namespace_dict(element):
    return element.nsmap


def get_namespace_prefix(element):
    return element.prefix


def get_sourceline(element):
    return element.sourceline


def get_tag(element):
    prefixed_tag = get_tag_with_namespace(element)
    return prefixed_tag.split("}")[-1]


def get_tags(elements):
    tags = []
    for element in elements:
        tags.append(get_tag(element))
    return tags


def get_namespace(element):
    prefixed_tag = get_tag_with_namespace(element)
    return prefixed_tag.split("}")[0] + "}"


def get_tag_with_namespace(element):
    return element.tag


# def get_tail(element): # haven't found a tail yet!
#     return element.tail


def get_text(element):
    return element.text


def filter_elements_by_tags(elements, tags):
    filtered = []
    for element in elements:
        if get_tag(element) in tags:
            filtered.append(element)
    return filtered


### Booleans


def is_element(element):
    return etree.iselement(element)


### Output and stringify


def tree_to_string(tree):
    root = get_tree_root(tree)
    return element_to_string(root)


def element_to_string(element):
    return etree.tostring(element, pretty_print=True)


def tree_to_file(tree, file):
    tree.write(file)


### Unsorted and untested


def CreateElement(tag):
    return etree.Element(tag)


def add_sub_element_to_element(child_element, element):
    child_copy = copy.deepcopy(child_element)
    element.append(child_copy)


def insert_sub_element_to_element_at_index(child_element, element, index):
    child_copy = copy.deepcopy(child_element)
    element.insert(index, child_copy)
