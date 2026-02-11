import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

class RadarPPI:
    def __init__(self, alcance_max=80):
        """
        Inicializa o radar PPI (Plan Position Indicator)
        
        :param alcance_max: alcance máximo em km
        """
        self.alcance_max = alcance_max
        self.fig, self.ax = plt.subplots(figsize=(10, 10), facecolor='black')
        self.angulo_varredura = 0
        self.alvos = []  # Lista para armazenar os alvos
        
        plt.style.use('dark_background')
        self.fig.patch.set_facecolor('black')
        
    def configurar_display(self):
        """Configura o display circular do radar"""
        self.ax.clear()

        # Fundo verde radar (RGB típico de displays antigos)
        verde_radar = '#00FF41'  # Verde fosforescente
        verde_escuro = '#003B00'  # Verde mais escuro para grades
        
        # Área do radar (círculo principal)
        radar_area = Circle((0, 0), self.alcance_max, 
                          facecolor='black', edgecolor=verde_radar, linewidth=2)
        self.ax.add_patch(radar_area)
        
        # Desenhar círculos de alcance
        for r in range(0, self.alcance_max + 1, 20):
            circle = Circle((0, 0), r, fill=False, linestyle='--', linewidth=0.5, alpha=0.7)
            self.ax.add_patch(circle)
            if r > 0:
                self.ax.text(r, 0, f'{r}km', color=verde_radar,  verticalalignment='center', fontsize=9, fontfamily='monospace')
        
        # Desenhar linhas de azimute
        for angle in range(0, 360, 30):
            rad = np.radians(angle)
            x = self.alcance_max * np.cos(rad)
            y = self.alcance_max * np.sin(rad)
            self.ax.plot([0, x], [0, y], '--', color=verde_escuro, linewidth=0.5, alpha=0.3)
            self.ax.text(x*1.2, y*1.05, f'{angle}°', color=verde_radar, ha='center', va='center', fontfamily='monospace')
        
        # Configurar limites e aspecto
        self.ax.set_xlim(-self.alcance_max*1.1, self.alcance_max*1.1)
        self.ax.set_ylim(-self.alcance_max*1.1, self.alcance_max*1.1)
        self.ax.axis('off')
        self.ax.set_title('U.V.', pad=20, fontsize=14, fontweight='bold', fontfamily='monospace')
    
    def carregar_alvos(self, dados_alvos, distancia_tolerancia_km=1, velocidade_tolerancia=12.5):
        
        if not dados_alvos:
            self.alvos = []
            return
            
        # Converte para numpy array e distância para km
        dados = np.array(dados_alvos)
        dados[:, 0] /= 1000  # Converte distância para km
        
        
        # Agrupa alvos próximos
        grupos = []
        usado = np.zeros(len(dados), dtype=bool)
        
        for i, (dist, vel) in enumerate(dados):
            if not usado[i]:
                # Encontra todos os alvos próximos a este
                mask = (np.abs(dados[:, 0] - dist)) < distancia_tolerancia_km
                mask &= (np.abs(dados[:, 1] - vel)) < velocidade_tolerancia
                mask &= ~usado
                
                # Calcula a média do grupo
                if np.any(mask):
                    grupo = dados[mask]
                    media_dist = np.mean(grupo[:, 0]) * 1000  # Converte de volta para metros
                    media_vel = np.mean(grupo[:, 1])
                    if media_vel > 0:
                        media_vel = -(media_vel-velocidade_tolerancia)
                    else:
                        media_vel = -media_vel+velocidade_tolerancia
                    media_vel = -media_vel
                    grupos.append([media_dist, media_vel])
                    usado[mask] = True
        
        # Processa os alvos agrupados
        self.alvos = []
        for i, (distancia, velocidade) in enumerate(grupos):
            # Gerar ângulo aleatório para distribuição circular
            azimuth = np.random.uniform(0, 360)

            # Converter para coordenadas cartesianas
            x = (distancia / 1000) * np.cos(np.radians(azimuth))
            y = (distancia / 1000) * np.sin(np.radians(azimuth))
            
            # Armazenar alvo com ID único
            self.alvos.append({
                'id': i+1,
                'x': x,
                'y': y,
                'distancia': distancia,
                'velocidade': velocidade,
                'azimuth': azimuth,
                'num_deteccoes': sum(mask)  # Número de detecções agrupadas
            })
    
    def plotar_alvos(self):
        """Plota todos os alvos no display do radar"""
        for alvo in self.alvos:
            # Determinar cor baseada na velocidade (opcional)
            cor = self._cor_pela_velocidade(alvo['velocidade'])
            
            # Plotar o alvo
            if alvo['velocidade'] != 0:
                self.ax.plot(alvo['x'], alvo['y'], 'o', color=cor, markersize=8)
                
                # Adicionar informações do alvo
                info = f"ID: {alvo['id']}\nDist: {alvo['distancia']/1000:.1f}km\nVel: {alvo['velocidade']:.1f}m/s"
                self.ax.text(alvo['x'], alvo['y']+3, info, 
                            fontsize=8, color='white', 
                            bbox=dict(facecolor=cor, alpha=0.7),
                            ha='center')
                
    def _cor_pela_velocidade(self, velocidade):
        """Retorna cor baseada na velocidade (opcional)"""
        if abs(velocidade) < 100:
            return 'green'  # Baixa velocidade
        elif abs(velocidade) < 300:
            return 'yellow'  # Velocidade média
        else:
            return 'red'  # Alta velocidade
    
    def atualizar_varredura(self, angulo_incremento=3):
        """Atualiza o ângulo de varredura e redesenha"""
        self.angulo_varredura = (self.angulo_varredura - angulo_incremento) % 360
        self.configurar_display()
        self.plotar_alvos()
        
        # Desenhar linha de varredura
        x_end = self.alcance_max * np.cos(np.radians(self.angulo_varredura))
        y_end = self.alcance_max * np.sin(np.radians(self.angulo_varredura))
        self.ax.plot([0, x_end], [0, y_end], 'g-', linewidth=1, alpha=0.5)
        
        self.ax.set_aspect('equal')
        #plt.pause(0.05)
