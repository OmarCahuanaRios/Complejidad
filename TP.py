import tkinter
import graphviz as gv
import networkx as nx
from io import open
import heapq as hq
import math






archivo=open("emeplo.txt","r",encoding="utf-8")
texto=archivo.readlines()
archivo.close()
ventana=tkinter.Tk()


ventana.title("TSP")
ventana.geometry("800x800")





def nx2gv(G, weighted=False, params={'rankdir': 'LR', 'size': '5'},
          path=None, pathparams={'color': 'orangered'}, nodeinfo=False):
    if G.is_directed():
        g = gv.Digraph('G')
    else:
        g = gv.Graph('G')
    g.attr(**params)

    for i in range(G.number_of_nodes()):
        if nodeinfo:
            g.node(str(i), **dict(G.nodes[i]))
        else:
            g.node(str(i))

    for u, v in G.edges():
        pp = pathparams if path and path[v] == u else {}

        if weighted:
            g.edge(str(u), str(v), f"{G.edges[u, v]['weight']}", **pp)
        else:
            g.edge(str(u), str(v), **pp)

    return g


def adjmatrix2gv(G, weighted=False, params={'rankdir': 'LR', 'size': '5'}):
    return nx2gv(nx.from_numpy_matrix(G), weighted, params)


def adjlist2gv(G, type='digraph', weighted=False, params={'rankdir': 'LR'}):
    digraph = type == 'digraph'
    if digraph:
        g = gv.Digraph('G')
    else:
        g = gv.Graph('G')
    Gv.attr(**params)

    n = len(G)
    for i in range(n):
        g.node(str(i))

    for u in range(n):
        if weighted:
            for v, w in range(n):
                g.edge(str(u), str(v), str(w))
                if digraph:
                    g.edge(str(v), str(u), str(w))
        else:
            for v in range(n):
                g.edge(str(u), str(v))
                if digraph:
                    g.edge(str(v), str(u))

    return g


def path2gv(path, params={'rankdir': 'LR', 'size': '5'}):
    g = gv.Digraph('G')
    g.attr(**params)

    n = len(path)
    for i in range(n):
        g.node(str(i))

    for v, u in enumerate(path):
        if u != -1:
            g.edge(str(u), str(v))

    return g


def wedges2adjlist(filename: str, type='graph'):
    with open(filename) as file:
        data = []
        n = 0
        for line in file:
            if line[0] != '#':
                data.append([int(x) for x in line.strip().split(',')])
                if data[-1][0] > n: n = data[-1][0]
                if data[-1][1] > n: n = data[-1][1]

    n += 1
    G = [[] for _ in range(n)]
    for u, v, w in data:
        G[u].append((v, w))
        if type == 'graph':
            G[v].append((u, w))

    return G







def proyecto():
    NDepartamento = Apartamento.get()
    NProvincia = Provincia.get()
    NDistrito = Distrito.get()
    NCentroPoblado = CentroPoblado.get()
    Nodo = [NDepartamento, NProvincia, NDistrito, NCentroPoblado]

    def dijkstra(G, s):
        for u in G.nodes:
            G.nodes[u]['visited'] = False
            G.nodes[u]['path'] = -1
            G.nodes[u]['cost'] = math.inf
            cost = []

        G.nodes[s]['cost'] = 0
        q = [(0, s)]
        while q:
            g_u, u = hq.heappop(q)
            if not G.nodes[u]['visited']:
                G.nodes[u]['visited'] = True
                for v in G.neighbors(u):
                    if not G.nodes[v]['visited']:
                        w_uv = G.edges[u, v]['weight']
                        f_v = g_u + w_uv
                        g_v = G.nodes[v]['cost']
                        if f_v < g_v:
                            G.nodes[v]['cost'] = f_v
                            G.nodes[v]['path'] = u
                            hq.heappush(q, (f_v, v))

        path = [0] * G.number_of_nodes()
        for v, info in G.nodes.data():
            path[v] = info['path']
            cost.append(G.nodes[v]['cost'])

        return path, cost


#1


    archivo = open("emeplo.txt", "r",encoding="utf-8")
    texto = archivo.readlines()
    ciudad=0
    listaCompleta = []
    coordenadas = []

    distancias = [[0 for i in range(len(texto))] for i in range(len(texto))]
    archivo.close()
    for i in texto:
        arreglo = i
        listaCompleta.append(arreglo.split(","))

    for i in range(len(listaCompleta)):
        coordenadas.append([float(listaCompleta[i][4]), float(listaCompleta[i][5])])

    for i in range(len(texto)):
        pivote = coordenadas[i]
        for j in range(len(texto)):
            if (i != j):
                distancias[i][j] = math.sqrt(
                    (pivote[0] - coordenadas[j][0]) ** 2 + (pivote[1] - coordenadas[j][1]) ** 2)

    f = open("DPA.txt", "w",encoding="utf-8")

    for i in range(len(distancias)):
        for j in range(len(distancias)):
            if (i != j):
                f.write(str(i))
                f.write(',')
                f.write(str(j))
                f.write(',')
                f.write(str(distancias[i][j]))
                f.write('\n')

    f.close()
    arreglo2=[]
    for i in range(len(arreglo2)):
        if([arreglo2[i][0], arreglo2[i][1],arreglo2[i][2], arreglo2[i][3]]==Nodo):
            ciudad=i
            Destino["text"]= f"La ciudad elegida es el nodo:{i}\n"


    G2 = nx.read_weighted_edgelist('DPA.txt', create_using=nx.Graph, delimiter=',', nodetype=int)
    path, cost = dijkstra(G2, ciudad)
    Ipath["text"]=path
    for i in cost:
        print(i)
        Icost["text"] += f"{i} \n"



def LL():
    etiqueta2["text"]="DEPARTAMENTO | PRONCIA | DISTRITO | CENTRO POBLADO | LATITUD | LONGITUD"

    arreglo2 = []
    for i in texto:
        arreglo = i
        arreglo2.append(arreglo.split(","))

    for i in range(len(arreglo2)):
        etiqueta["text"]+=f"{arreglo2[i][0]} | {arreglo2[i][1]} | {arreglo2[i][2]} | {arreglo2[i][3]} | {arreglo2[i][4]} | {arreglo2[i][5]} \n"




def salir():
    exit(0)

def TSP():

    NDepartamento=Apartamento.get()
    NProvincia=Provincia.get()
    NDistrito=Distrito.get()
    NCentroPoblado=CentroPoblado.get()
    Nodo=[NDepartamento,NProvincia,NDistrito,NCentroPoblado]



    arreglo2 = []
    for i in texto:
        arreglo=i
        arreglo2.append(arreglo.split(","))
    for i in range(len(arreglo2)):
        if([arreglo2[i][0], arreglo2[i][1],arreglo2[i][2], arreglo2[i][3]]==Nodo):
            Destino["text"]= f"La ciudad elegida es el nodo:{i}\n"







    for a,b,c,d,e,f,g,h in arreglo2:
        if(a==NDepartamento and b==NProvincia and c==NDistrito and d== NCentroPoblado):
           Destino["text"]+=f"{NDepartamento} {NProvincia} {NDistrito} {NCentroPoblado} y sus latitudes son: {e}{f} \n"






def CREDITOS():
    etiqueta["text"]="Desarrollado por Omar Cahuana Rios - Ciclo 2021 I"

def ObtenerCreditos():

    return

A=tkinter.Label(ventana)
A["text"]="Ingresa Departamento"
A.pack()
Apartamento=tkinter.Entry(ventana)
Apartamento.pack()

P=tkinter.Label(ventana)
P["text"]="Ingresa Provincia"
P.pack()
Provincia=tkinter.Entry(ventana)
Provincia.pack()


D=tkinter.Label(ventana)
D["text"]="Ingresa Distrito"
D.pack()
Distrito=tkinter.Entry(ventana)
Distrito.pack()


CP=tkinter.Label(ventana)
CP["text"]="Ingresa Centro Poblado"
CP.pack()
CentroPoblado=tkinter.Entry(ventana)
CentroPoblado.pack()



boton2=tkinter.Button(ventana,text="Ver Origen",command=TSP)
boton2.pack()
Destino=tkinter.Label(ventana)
Destino.pack()
boton3=tkinter.Button(ventana,text="Implementar Proyecto",command=proyecto)
boton3.pack()
Ipath=tkinter.Label(ventana)
Ipath.pack()
Icost=tkinter.Label(ventana)
Icost.pack()




boton5=tkinter.Button(ventana,text="Obtener solo Longitud, latitud y distancia",command=LL)
boton5.pack()

boton3=tkinter.Button(ventana,text="Créditos",command=CREDITOS)
boton3.pack()
boton1=tkinter.Button(ventana,text="Salir",command=salir)
boton1.pack()
etiqueta2=tkinter.Label(ventana)
etiqueta2.config(fg="blue",font=("Verdana",20))
etiqueta2.pack()
etiqueta=tkinter.Label(ventana)
etiqueta.config(font=("Verdana",15))
etiqueta.pack()
ventana.mainloop()








