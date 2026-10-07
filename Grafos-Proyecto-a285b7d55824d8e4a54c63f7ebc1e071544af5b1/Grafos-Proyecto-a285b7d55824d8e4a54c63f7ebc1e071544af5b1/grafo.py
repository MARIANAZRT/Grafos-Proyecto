#LIBRERIAS:
import networkx as nx
from pyvis.network import Network
import webbrowser
import os

def crear_grafo_interactivo():
    print("=" * 55)
    print("   CONSTRUCTOR INTERACTIVO DE GRAFOS Y EMPAREJAMIENTO")
    print("=" * 55)

    #SELECCIÓN DEL TIPO DE GRAFO
    print("\nSeleccione el tipo de grafo:")
    print("1. No dirigido")
    print("2. Dirigido")
    opcion = input("Opción: ").strip()
    if opcion == "2":
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    #INGRESO DE VÉRTICES
    print("\n--- INGRESO DE VÉRTICES (V) ---")
    print("Ingrese los vértices uno por uno.")
    print("Escriba 'FIN' para terminar.")
    i = 1
    while True:
        v = input(f"Vértice {i}: ").strip()
        if v.upper() == "FIN" or v == "":
            if G.number_of_nodes() == 0:
                print("Debe ingresar al menos un vértice.")
                continue
            break
        G.add_node(v)
        i += 1

    #INGRESO DE ARISTAS
    print("\n--- INGRESO DE ARISTAS / ARCOS (A) ---")
    print("Ingrese las conexiones.")
    print("Escriba 'FIN' en el origen para terminar.")
    i = 1
    while True:
        print(f"\nArista {i}:")
        u = input("  Vértice Origen (u): ").strip()
        if u.upper() == "FIN" or u == "":
            break
        v = input("  Vértice Destino (v): ").strip()
        if v.upper() == "FIN" or v == "":
            break
        # Si el vértice no existía, se agrega
        if u not in G:
            G.add_node(u)
        if v not in G:
            G.add_node(v)
        G.add_edge(u, v)
        i += 1
    return G
def calcular_y_visualizar(G):
    if G.number_of_nodes() == 0:
        print("\nEl grafo está vacío.")
        return

    #CALCULAR GRADOS Y BUCLES
    grados = {}
    bucles = {}
    for nodo in G.nodes():
        # Grado del vértice
        grados[nodo] = G.degree(nodo)
        # Cantidad de bucles
        bucles[nodo] = G.number_of_edges(nodo, nodo)

    #CALCULAR EMPAREJAMIENTO
    emparejamiento = set()
    tipo_emparejamiento = "No aplicable"
    if not G.is_directed():
        # Se crea una copia para el matching
        # y se eliminan los bucles.
        G_matching = G.copy()
        G_matching.remove_edges_from(
            nx.selfloop_edges(G_matching)
        )
        emparejamiento = nx.max_weight_matching(
            G_matching,
            maxcardinality=True
        )
    # --- CLASIFICACIÓN ---
        nodos_cubiertos = len(emparejamiento) * 2
        total_nodos = G.number_of_nodes()
        
        if nodos_cubiertos == 0:
            tipo_emparejamiento = "No hay aristas válidas"
        elif nodos_cubiertos == total_nodos:
            tipo_emparejamiento = "Perfecto (y Máximo/Maximal)"
        else:
            tipo_emparejamiento = "Máximo (y Maximal)"
    else:
        tipo_emparejamiento = "N/A (Grafo Dirigido)"
    #CREAR RED PYVIS
    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#1e1e1e",
        font_color="white"
    )

    #AGREGAR LOS VÉRTICES DEL GRAFO REAL
    for nodo in G.nodes():
        net.add_node(
            nodo,
            label=str(nodo),
            title=(
                f"Vértice: {nodo}"
                f"<br>Grado: {grados[nodo]}"
                f"<br>Bucles: {bucles[nodo]}"
            ),
            color="#4aa3df",
            size=25
        )

    #AGREGAR LAS ARISTAS DEL GRAFO REAL
    parejas_matching = set(emparejamiento)
    for u, v in G.edges():
        es_matching = (
            (u, v) in parejas_matching
            or
            (v, u) in parejas_matching
        )
        if es_matching:
            net.add_edge(
                u,
                v,
                title="EMPAREJADO",
                color="#ff4757",
                width=5
            )
        else:
            net.add_edge(
                u,
                v,
                color="#747d8c",
                width=1.5
            )
    # Activar movimiento del grafo
    net.toggle_physics(True)

    #CREAR EL HTML
    archivo_html = "grafo_interactivo.html"
    net.write_html(archivo_html)

    #INFORMACIÓN DEL GRAFO
    if G.is_directed():
        tipo_str = "Dirigido (DiGraph)"
    else:
        tipo_str = "No dirigido (Graph)"
    cantidad_vertices = G.number_of_nodes()
    cantidad_aristas = G.number_of_edges()

    #PROPIEDADES DE LOS VÉRTICES
    html_propiedades = ""
    for nodo in G.nodes():
        html_propiedades += f"""
        <li style="
            margin-bottom: 8px;
            line-height: 1.5;
        ">
            <b>Vértice {nodo}</b>
            <br>
            → Grado:
            <b>{grados[nodo]}</b>
            <br>
            → Bucles:
            <b>{bucles[nodo]}</b>
        </li>
        """

    #EMPAREJAMIENTO
    if emparejamiento:
        html_matching = ""
        for u, v in emparejamiento:

            html_matching += f"""
            <li>
                <b>{u}</b>
                &lt;---&gt;
                <b>{v}</b>
            </li>
            """
    elif G.is_directed():
        html_matching = """
        <li>
            <i>
                No disponible para grafos dirigidos.
            </i>
        </li>
        """
    else:
        html_matching = """
        <li>
            <i>
                No se encontraron emparejamientos.
            </i>
        </li>
        """
    #PANEL DE INFORMACIÓN
    panel_html = f"""
    <div id="info-panel"
        style="
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 999;
            background-color:
                rgba(30, 30, 30, 0.94);
            color: #ffffff;
            padding: 18px;
            border-radius: 10px;
            font-family:
                'Segoe UI',
                Tahoma,
                Geneva,
                Verdana,
                sans-serif;
            box-shadow:
                0px 4px 12px
                rgba(0,0,0,0.5);
            border: 1px solid #444;
            max-width: 330px;
            max-height: 90vh;
            overflow-y: auto;
        "
    >
        <h2 style="
            margin-top: 0;
            color: #4aa3df;
            font-size: 18px;
            border-bottom:
                1px solid #444;
            padding-bottom: 8px;
        ">
            Información del Grafo

        </h2>
        <p style="margin: 6px 0;">
            <b>Tipo:</b>
            {tipo_str}
        </p>
        <p style="margin: 6px 0;">
            <b>Vértices |V|:</b>
            {cantidad_vertices}
        </p>
        <p style="margin: 6px 0;">

            <b>Aristas |A|:</b>
            {cantidad_aristas}
        </p>
        <h3 style="
            color: #4aa3df;
            font-size: 15px;
            margin-top: 18px;
            margin-bottom: 8px;
        ">
            Propiedades de los vértices
        </h3>
        <ul style="
            margin: 0;
            padding-left: 20px;
            color: #dddddd;
            font-size: 14px;
        ">
            {html_propiedades}
        </ul>
        <h3 style="
            color: #ff4757;
            font-size: 15px;
            margin-top: 18px;
            margin-bottom: 8px;
        ">
            Emparejamiento Óptimo
        </h3>
        <p style="margin: 0 0 8px 0; color: #2ed573; font-size: 13px;">
            <b>Clasificación:</b> {tipo_emparejamiento}
        </p>
        <ul style="
            margin: 0;
            padding-left: 20px;
            color: #dddddd;
            font-size: 14px;
        ">
            {html_matching}
        </ul>
    </div>
    """
    #INSERTAR EL PANEL EN EL HTML GENERADO
    with open(
        archivo_html,
        "r",
        encoding="utf-8"
    ) as archivo:
        contenido_html = archivo.read()
    contenido_html = contenido_html.replace(
        "</body>",
        panel_html + "</body>"
    )
    with open(
        archivo_html,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido_html)

    #ABRIR EL GRAFO
    print()
    print("=" * 55)
    print("GRAFO GENERADO CORRECTAMENTE")
    print("=" * 55)
    print(f"Vértices: {cantidad_vertices}")
    print(f"Aristas: {cantidad_aristas}")
    print(
        f"\nArchivo generado: {archivo_html}"
    )
    ruta_absoluta = os.path.abspath(
        archivo_html
    )
    webbrowser.open(
        f"file://{ruta_absoluta}"
    )
#PROGRAMA PRINCIPAL
if __name__ == "__main__":
    grafo_usuario = crear_grafo_interactivo()
    calcular_y_visualizar(grafo_usuario)