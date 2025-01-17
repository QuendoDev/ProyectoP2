# Resultados de las simulaciones hechas con el supercomputador de la UGR del codigo de la primera parte
# de vol_main.py para N = [16, 32, 64, 128] y para T = np.linspace(1.5, 3.5, 10), además de usar los indices
# para la funcion de correlacion i = [1, 3].

import numpy as np
import os

import vol.setup.constants as cte

E = np.array([
    # N = 16
    [-15.6109375, -15.13125, -14.254675, -12.76145, -10.1841875,
     -8.2414125, -7.1513375, -6.362825, -5.775075, -5.270675],
    # N = 32
    [-31.2153125, -30.256, -28.52774375, -25.434625, -19.65610625,
     -16.32123125, -14.2682875, -12.722425, -11.53499375, -10.56535625],
    # N = 64
    [-62.434446875, -60.49568125, -57.064409375, -50.8872375, -38.925934375,
     -32.670546875, -28.52565625, -25.463278125, -23.0607, -21.106878125],
    # N = 128
    [-124.879821875, -120.977109375, -114.1093671875, -101.7854984375, -77.8765234375,
     -65.308325, -57.0629125, -50.951875, -46.134303125, -42.2496484375]
])

c = np.array([
    # N = 16
    [0.29511015624999953, 0.6186737903226311, 1.2337393255713518, 2.485834887692328, 3.458859534156971,
     2.048978784015965, 1.4503655627205825, 1.1747354980909037, 0.982162366016946, 0.8739579078571426],
    # N = 32
    [0.2995059895832431, 0.6229794919354976, 1.2205498884910413, 2.602719836538409, 3.2618733665625514,
     1.8553582813763163, 1.4128598450735461, 1.1489131153636747, 0.9672111800370843, 0.8746455870981923],
    # N = 64
    [0.2896894653907414, 0.6194179704750328, 1.2654184154272246, 2.690213310289647, 2.8258203368299037,
     1.8130365265543777, 1.3903805500919109, 1.1324705624873208, 0.990787836355825, 0.857634392845869],
    # N = 128
    [0.2958045351794378, 0.6178173245373932, 1.2212870925066195, 2.6501542835299357, 2.8455763873444506,
     1.8234492951079564, 1.3876183948893468, 1.1530088565337462, 0.9584430644051389, 0.85390808977406]
])

fcorr0 = np.array([
    # N = 16
    [0.975709375, 0.9457953125, 0.8909359375, 0.7978109375, 0.6366515625,
     0.514984375, 0.4469828125, 0.3973203125, 0.3612296875, 0.329371875],
    # N = 32
    [0.975432421875, 0.9454875, 0.891479296875, 0.794847265625, 0.6143359375,
     0.510221875, 0.446046875, 0.39747265625, 0.3606875, 0.330060546875],
    # N = 64
    [0.97552880859375, 0.9452576171875, 0.8916404296875, 0.7951162109375, 0.6082427734375,
     0.5104826171875, 0.4457048828125, 0.39784482421875, 0.36032783203125, 0.32991044921875],
    # N = 128
    [0.9756295654296875, 0.945126220703125, 0.891482763671875, 0.7951860107421875, 0.608412841796875,
     0.5101510498046875, 0.4458111083984375, 0.398025146484375, 0.36042587890625, 0.3300767578125]
])

fcorr1 = np.array([
    # N = 16
    [0.9734265625, 0.937003125, 0.8622234375, 0.7133828125, 0.41543125,
     0.2164453125, 0.134825, 0.09213125, 0.0670046875, 0.050059375],
    # N = 32
    [0.973096875, 0.936775390625, 0.863384765625, 0.70755546875, 0.361418359375,
     0.20304921875, 0.13269921875, 0.0918640625, 0.0663671875, 0.049380078125],
    # N = 64
    [0.9731892578125, 0.93642841796875, 0.8636279296875, 0.7082232421875, 0.34658125,
     0.203955859375, 0.1328423828125, 0.0917279296875, 0.06638046875, 0.04972373046875],
    # N = 128
    [0.973292138671875, 0.9363243408203125, 0.863441015625, 0.7084792236328125, 0.3466463623046875,
     0.203462353515625, 0.132902197265625, 0.0919744140625, 0.0666431396484375, 0.049748974609375]
])


# Voy a guardar esto y los valores de Onsager y de la funcion de correlacion que faltan en un archivo .npy para
# adaptar el codigo de la segunda parte de vol_main.py a estos valores, ya que este archivo solo se usó para
# realizar el informe del ejercicio y no será lo que se entregue. Primero cargo los datos de magnetizacion y correlacion
# extra que se generaron en cte.ANALYSIS_PATH/Datos y finalmente guardo todos los datos juntos en un archivo .npy para
# cada N y cada T en cte.DATA_PATH.
def format_data():
    mag = np.load(os.path.join(cte.ANALYSIS_PATH, 'Datos', 'mag.npy'))
    print('mag', mag, mag.shape)
    corr = np.load(os.path.join(cte.ANALYSIS_PATH, 'Datos', 'corr.npy'))
    print('corr', corr, corr.shape)

    print('E', E.shape)
    print('c', c.shape)
    print('fcorr0', fcorr0.shape)
    print('fcorr1', fcorr1.shape)

    # Creo un array para cada N y cada T con los valores de magnetizacion, energia, calor especifico y correlaciones.
    for N in range(len(cte.N)):
        Ne = cte.N[N]
        for T in range(len(cte.T)):
            Te = cte.T[T]
            result = np.array([mag[N][T], E[N][T], c[N][T], fcorr0[N][T], fcorr1[N][T], corr[N][2][T], corr[N][3][T]])
            np.save(os.path.join(cte.DATA_PATH, f'{Ne}_{Te}.npy'), result)

    # Leo e imprimo los datos guardados para verificar que funcionó correctamente.
    for N in range(len(cte.N)):
        Ne = cte.N[N]
        for T in range(len(cte.T)):
            Te = cte.T[T]
            result = np.load(os.path.join(cte.DATA_PATH, f'{Ne}_{Te}.npy'))
            print(f'{Ne}_{Te}.npy', result, result.shape)