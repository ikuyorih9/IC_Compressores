import matplotlib.pyplot as plt

def plot_ncd_average_graph(x1_values, x2_values, x_axis, title, x_label, y_label, y_lim=[0,1]):
  # Criar o gráfico de barras
  bar_width = 0.35  # Largura das barras
  index = range(len(x_axis))  # Índices para o eixo X

  # Plotando as barras
  fig, ax = plt.subplots(figsize=(6, 4))

  # Plotando as barras para DEFEITO e NÃO-DEFEITO
  bar1 = ax.bar(index, x1_values, bar_width, label='DEFEITO', color='red')
  bar2 = ax.bar([i + bar_width for i in index], x2_values, bar_width, label='NÃO-DEFEITO', color='green')

  for bar in bar1:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # Coordenada X (meio da barra)
        height,  # Coordenada Y (altura da barra)
        f'{height:.3f}',  # Texto com valor formatado
        ha='center', va='bottom', fontsize=10, color='black', rotation=90
    )

  for bar in bar2:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # Coordenada X (meio da barra)
        height,  # Coordenada Y (altura da barra)
        f'{height:.3f}',  # Texto com valor formatado
        ha='center', va='bottom', fontsize=10, color='black', rotation=90
    )

  # Ajustes para o gráfico
  ax.set_xlabel(x_label, fontsize=12)
  ax.set_ylabel(y_label, fontsize=12)
  ax.set_title(title, fontsize=14)
  ax.set_xticks([i + bar_width / 2 for i in index])
  ax.set_xticklabels(x_axis, rotation=45, ha='right')
  ax.legend()
  ax.set_ylim(y_lim[0], y_lim[1])

  # Exibir o gráfico
  plt.tight_layout()
  plt.show()

def zlib_print_all_graphs(dataset, x_axis, y_lim=[0.7,1.2]):
  for i in range(len(dataset)):
    level = dataset[i][0][0]
    window = dataset[i][0][1]
    mem = dataset[i][0][2]
    strategy = dataset[i][0][3]
    print(f"COMPRESSÃO NÍVEL {level},  MEMÓRIA {mem}, JANELA: {window}, ESTRATÉGIA: {strategy}")
    print(f"\tTempo de processamento = {dataset[i][1]:.3f} [s]")
    print(f"\tDiferença absoluta média = {dataset[i][2]:.3f}")
    plot_ncd_average_graph(
        dataset[i][3][0],
        dataset[i][3][1],
        x_axis,
        'ZLIB: diferença média NCD de nível ' + str(level) + ', memória ' + str(mem) + ', janela ' + str(window) + ', estratégia ' + str(strategy),
        'Arquivo com código defeituoso',
        'Média da NCD',
        y_lim=y_lim)
    
def ppmd_print_all_graphs(dataset, x_axis, y_lim=[0.7,1.2]):
  for i in range(len(dataset)):
    order = dataset[i][0]
    mem = dataset[i][1]
    print(f"COMPRESSÃO DE ORDEM {order} e MEMÓRIA {mem}:")
    print(f"\tTempo de processamento = {dataset[i][2]:.3f} [s]")
    print(f"\tDiferença absoluta média = {dataset[i][3]:.3f}")
    plot_ncd_average_graph(
        dataset[i][4][0],
        dataset[i][4][1],
        x_axis,
        'PPMd: média NCD para ordem ' + str(order) + ' e memória ' + str(mem) + ' KB',
        'Arquivo com código defeituoso',
        'Média da NCD',
        y_lim=y_lim)