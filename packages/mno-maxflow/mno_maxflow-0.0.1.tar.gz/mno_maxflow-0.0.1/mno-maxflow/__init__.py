class vertex:
    def __init__(self, name, source=False, sink=False):
        self.name = name
        self.source = source
        self.sink = sink

class edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.returnEdge = None

class create_flow_network:
    def __init__(self):
        self.vertices = []
        self.network = {}

    def get_source(self):
        for vertex in self.vertices:
            if vertex.source == True:
                return vertex
        return None

    def get_sink(self):
        for vertex in self.vertices:
            if vertex.sink == True:
                return vertex
        return None

    def get_vertex(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                return vertex

    def vertex_in_network(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return True
        return False

    def get_edges(self):
        allEdges = []
        for vertex in self.network:
            for edge in self.network[vertex]:
                allEdges.append(edge)
        return allEdges

    def create_vertex(self, name, source=False, sink=False):
        if source == True and sink == True:
            return "El nodo {} no puede ser origen y destino".format(name)
        if self.vertex_in_network(name):
            return "Nodo duplicado"
        if source == True:
            if self.get_source() != None:
                return "Ya existe nodo origen"
        if sink == True:
            if self.get_sink() != None:
                return "Ya existe nodo destino"
        newVertex = vertex(name, source, sink)
        self.vertices.append(newVertex)
        self.network[newVertex.name] = []

    def create_edge(self, start, end, capacity):
        if start == end:
            return "No se puede tener bucles"
        if self.vertex_in_network(start) == False:
            return "Nodo origen ya ha sido agregado"
        if self.vertex_in_network(end) == False:
            return "Nodo destino ya ha sido agregado"
        newEdge = edge(start, end, capacity)
        returnEdge = edge(end, start, 0)
        newEdge.returnEdge = returnEdge
        returnEdge.returnEdge = newEdge
        vertex = self.get_vertex(start)
        self.network[vertex.name].append(newEdge)
        returnVertex = self.get_vertex(end)
        self.network[returnVertex.name].append(returnEdge)

    def get_path(self, start, end, path):
        if start == end:
            return path
        for edge in self.network[start]:
            residualCapacity = edge.capacity - edge.flow
            if residualCapacity > 0 and not (edge, residualCapacity) in path:
                result = self.get_path(edge.end, end, path + [(edge, residualCapacity)])
                if result != None:
                    return result

    def MaxFlow(self):
        source = self.get_source()
        sink = self.get_sink()
        if source == None or sink == None:
            return "La red no tiene nodo origen y destido "
        path = self.get_path(source.name, sink.name, [])
        while path != None:
            flow = min(edge[1] for edge in path)
            for edge, res in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            path = self.get_path(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])

