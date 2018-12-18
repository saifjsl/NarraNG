import json


class NodeEncoder(json.JSONEncoder):

    @staticmethod
    def decode_qrange(qr):
        return {
            'minv': qr.minv,
            'maxv': qr.maxv,
            'dist': qr.dist
        }

    def default(self, o):
        if isinstance(o, LinkNode):
            return {'name': o.name, 'bound': o.bound, 'links': o.links, 'weight': o.weight, 'qrange': NodeEncoder.decode_qrange(o.qrange)}
        elif isinstance(o, LeafNode):
            return {'name': o.name, 'weight': o.weight}
        else:
            return json.JSONEncoder.default(self, o)


class NodeDecoder:

    @staticmethod
    def create_qrange(content):
        return QRange(content['minv'], content['maxv'], content['dist'])

    @staticmethod
    def node_generator(links, root):
        for link in links:
            if 'bound' in link:
                node = LinkNode(root, link['name'], link['bound'], link['weight'], NodeDecoder.create_qrange(link['qrange']))
                sublinks = NodeDecoder.node_generator(link['links'], node)
                node.links = list(sublinks)
                yield node
            else:
                node = LeafNode(root, link['name'], link['weight'])
                yield node

    @staticmethod
    def decode(file):
        root_node = json.load(file)
        name = root_node['name']
        bound = root_node['bound']
        weight = root_node['weight']
        qrange = NodeDecoder.create_qrange(root_node['qrange'])
        root = LinkNode(None, name, bound, weight, qrange)
        root.root = root
        root_links = list(NodeDecoder.node_generator(root_node['links'], root))
        root.links = root_links
        return root


class QRange:
    def __init__(self, minv, maxv, dist):
        self.minv = minv
        self.maxv = maxv
        if dist not in ['u', 'n', 't']:
            raise Exception('Created QRange with invalid dist. Can be only t or n. Received %s' % dist)
        self.dist = dist


class Node:
    def __init__(self, root, name, weight):
        super(Node, self).__init__()
        self.root = root
        self.name = name
        if type(weight) != float:
            raise Exception('Node weight must be float')
        self.weight = weight

    def __repr__(self):
        return self.name


class LinkNode(Node):
    MAPPER = {
        's': 'single',
        'm': 'many',
        'a': 'all'
    }

    def __init__(self, root, name, bound, weight, qrange):
        lb = bound.lower()
        if lb not in list(LinkNode.MAPPER.keys()) + list(LinkNode.MAPPER.values()):
            raise Exception('LinkNode bound must be either single(s), many(m) or all(a)')
        super(LinkNode, self).__init__(root, name, weight)
        self.bound = LinkNode.MAPPER[lb] if lb in LinkNode.MAPPER.keys() else lb
        self.links = []
        self.qrange = qrange
        self.locked = False


class LeafNode(Node):
    def __init__(self, root, name, weight):
        super(LeafNode, self).__init__(root, name, weight)
