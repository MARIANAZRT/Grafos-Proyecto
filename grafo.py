import networkx as nx
from pyvis.network import Network
import webbrowser
import os

def crear_grafo_interactivo():
    print("="*55)
    print("   CONSTRUCTOR INTERACTIVO DE GRAFOS Y EMPAREJAMIENTO")
    print("="*55)

    # 1. Selección del tipo de grafo
    print("\nSeleccione el tipo de grafo:")
    print("1. No dirigido (nx.Graph)")
    print("2. Dirigido (nx.DiGraph)")
    
    opcion = input("Opción: ").strip()
    G = nx.DiGraph() if opcion == "2" else nx.Graph()

    # 2. Ingreso simple de Vértices
    print("\n--- INGRESO DE VÉRTICES (V) ---")
    print("Ingrese los vértices uno por uno. Escriba 'FIN' para terminar.")
    
    i = 1
    while True:
        v = input(f"Vértice {i}: ").strip()
        if v.upper() == 'FIN' or v == "":
            if G.number_of_nodes() == 0:
                print("Debe ingresar al menos un vértice.")
                continue
            break
        
        G.add_node(v, label=v)
        i += 1

    # 3. Ingreso simple de Aristas (sin peso)
    print("\n--- INGRESO DE ARISTAS / ARCOS (A) ---")
    print("Ingrese las conexiones. Escriba 'FIN' en el origen para terminar.")
    
    i = 1
    while True:
        print(f"\nArista {i}:")
        u = input("  Vértice Origen (u): ").strip()
        if u.upper() == 'FIN' or u == "":
            break
        
        v = input("  Vértice Destino (v): ").strip()
        if v.upper() == 'FIN' or v == "":
            break

        # Si el usuario ingresa nodos que no estaban en V, se añaden automáticamente
        if u not in G:
            G.add_node(u, label=u)
        if v not in G:
            G.add_node(v, label=v)

        G.add_edge(u, v)
        i += 1

    return G

def calcular_y_visualizar(G):
    if G.number_of_nodes() == 0:
        print("\nEl grafo está vacío.")
        return

    # --- CÁLCULO DE EMPAREJAMIENTO ---
    emparejamiento = set()
    if not G.is_directed():
        # Emparejamiento cardinal máximo (sin pesos)
        emparejamiento = nx.max_weight_matching(G, maxcardinality=True)

    # --- GENERACIÓN DE VISUALIZACIÓN INTERACTIVA ---
    net = Network(height="100vh", width="100%", bgcolor="#1e1e1e", font_color="white")
    
    # Nodos
    for node in G.nodes():
        net.add_node(node, label=str(node), title=f"Vértice: {node}", color="#4aa3df", size=25)

    parejas_matching = set(emparejamiento)

    # Aristas
    for u, v in G.edges():
        es_matching = (u, v) in parejas_matching or (v, u) in parejas_matching

        if es_matching:
            net.add_edge(u, v, title="EMPAREJADO", color="#ff4757", width=5)
        else:
            net.add_edge(u, v, color="#747d8c", width=1.5)

    net.toggle_physics(True)
    
    archivo_html = "grafo_interactivo.html"
    net.write_html(archivo_html)

    # --- PREPARAR TEXTO Y HTML PARA INYECTAR EN LA WEB ---
    tipo_str = 'Dirigido (DiGraph)' if G.is_directed() else 'No dirigido (Graph)'
    nodes_cnt = G.number_of_nodes()
    edges_cnt = G.number_of_edges()
    
    if emparejamiento:
        html_matching = "".join([f"<li><b>{u}</b> &lt;---&gt; <b>{v}</b></li>" for u, v in emparejamiento])
        txt_matching = "\n".join([f" - {u} <---> {v}" for u, v in emparejamiento])
    elif G.is_directed():
        html_matching = "<i>No disponible para grafos dirigidos</i>"
        txt_matching = " No disponible para grafos dirigidos"
    else:
        html_matching = "<i>No se encontraron emparejamientos</i>"
        txt_matching = " Sin emparejamientos"

    panel_y_script_html = f"""
    <div id="info-panel" style="
        position: absolute;
        top: 20px;
        left: 20px;
        z-index: 999;
        background-color: rgba(30, 30, 30, 0.92);
        color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        border: 1px solid #444;
        max-width: 320px;
    ">
        <h2 style="margin-top: 0; color: #4aa3df; font-size: 18px; border-bottom: 1px solid #444; padding-bottom: 8px;">
            📊 Información del Grafo
        </h2>
        <p style="margin: 6px 0;"><b>Tipo:</b> {tipo_str}</p>
        <p style="margin: 6px 0;"><b>Vértices |V|:</b> {nodes_cnt}</p>
        <p style="margin: 6px 0;"><b>Aristas |A|:</b> {edges_cnt}</p>
        
        <h3 style="color: #ff4757; font-size: 15px; margin-top: 14px; margin-bottom: 6px;">
            🔴 Emparejamiento Óptimo
        </h3>
        <ul style="margin: 0; padding-left: 20px; color: #dddddd; font-size: 14px;">
            {html_matching}
        </ul>

        <button onclick="descargarReporte()" style="
            margin-top: 15px;
            width: 100%;
            padding: 8px;
            background-color: #2ed573;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 13px;
        ">📥 Descargar Resumen (.txt)</button>
    </div>

    <script>
    function descargarReporte() {{
        const contenido = `======================================\\n` +
                          `       REPORTE DEL GRAFO G = (V, A)   \\n` +
                          `======================================\\n` +
                          `Tipo de Grafo : {tipo_str}\\n` +
                          `Num Vértices  : {nodes_cnt}\\n` +
                          `Num Aristas   : {edges_cnt}\\n\\n` +
                          `EMPAREJAMIENTO ÓPTIMO:\\n` +
                          `{txt_matching}\\n`;
                          
        const blob = new Blob([contenido], {{ type: 'text/plain;charset=utf-8' }});
        const enlace = document.createElement('a');
        enlace.href = URL.createObjectURL(blob);
        enlace.download = 'reporte_grafo.txt';
        enlace.click();
    }}
    </script>
    </body>
    """

    with open(archivo_html, "r", encoding="utf-8") as f:
        contenido_html = f.read()

    contenido_modificado = contenido_html.replace("</body>", panel_y_script_html)

    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(contenido_modificado)

    print(f"\n¡Grafo e interfaz HTML actualizados en '{archivo_html}'!")
    
    ruta_absoluta = os.path.abspath(archivo_html)
    webbrowser.open(f"file://{ruta_absoluta}")

if __name__ == "__main__":
    grafo_usuario = crear_grafo_interactivo()
    calcular_y_visualizar(grafo_usuario)