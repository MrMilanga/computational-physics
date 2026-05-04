import numpy as np  
#Numpy ya trae la funcion de hacer transformada de fourier incluida
#Si no sabe importar numpy, primero tiene que ir al cmd y pone pip install numpy y alo mucho tendra que actualizarlo poniendo la secuencia python -m pip install --upgrade pip

import matplotlib.pyplot as plt #matplotlib sirve para graficar sobre todo, y se instala y actualiza como el anterior

plt.style.use('classic') #Aca le puede escribir muchos estilos, puede verlos en https://python-charts.com/es/matplotlib/estilos/

class Wave:
    def __init__(self):
        # Lista de parametros, donde voy a guardar la amplitud, el desfasaje y la frecuencia
        self.params = [np.random.rand(), np.random.rand(), np.random.rand()]#Aca le estoy diciendo que pueden ser aleatorio todo

    def evaluate(self, x): #Para el dominio de la onda, y basicamente traer los resultados, el x esta multiplicado para decirnos para que punto de X nos corresponde el punto de Y
        return self.params[0] * np.cos(self.params[1] + 2 * np.pi * x * self.params[2])#Puede cambiar en vez de tener coseno, tener un seno cambiando donde dice np.cos por np.sin
#primer params, es el desfase, y el parametro 2 es la frecuencia 

def main():
    n_waves = 12 # las ondas que se generan son completamente aleatorias, basicamente es una suma aleatoria de senos y cosenos

    waves = [Wave() for i in range(n_waves)]

    x = np.linspace(-10, 10, 500)#Dominio
    y = np.zeros_like(x)

    for wave in waves:
        y += wave.evaluate(x)   # "Y" va a ser las sumas de las ondas
#Si quiere puede visualizar esta onda que acabamos de crear usando plt.plot(Y) 
# plt.show()
    
    plt.plot(y)
    plt.show()
       
    # Transformada de fourier (funcion)

    f = np.fft.fft(y)
    freq = np.fft.fftfreq(len(y), d = x[1] - x[0])#con esto obtengo la frecuencia 

    fig, ax = plt.subplots(2)

    for wave in waves: #esto seria para ver todas las ondas que componen a mi onda genereda
        ax[0].plot(wave.evaluate(x), color = 'black', alpha = 0.2)

    ax[0].plot(y, color = 'blue')
    ax[1].plot(freq, abs(f)**2)# grafico la frecuencia, esta elevada al cuadrado, ya que es compleja y lo estoy graficando en reales 
    plt.show()


if __name__ == '__main__':
    main()