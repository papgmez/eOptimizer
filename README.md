## Sistema Inteligente para la Gestión y Optimización de Energía Basado en la Nube
El consumo de energía juega un papel fundamental en el progreso y bienestar de la sociedad. Tanto es así que la demanda de energía se multiplica con el paso del tiempo y por lo tanto, el precio de la misma. Además, las fuentes de energía fósiles son agotables y se debe ir apostando por medios de extracción de energías renovables tanto como sea posible. Para poder lidiar con ello se debería poder obtener energía de numerosas fuentes, dependiendo de varios factores que las condicionan y seleccionando la más adecuada en cada momento, sin depender de una única fuente energética para satisfacer la demanda como ocurre actualmente. Lamentablemente esto es ardúa tarea para el ser humano, pero alcanzable para la computación.

Este trabajo fin de grado consiste en la creación de un sistema inteligente para la gestión de energía en el hogar de la manera más óptima y eficiente posible. En función de un escenario determinado en cada hora del día, el sistema es capaz de modelar la cantidad de energía eléctrica recibida por cada una de las fuentes de entrada energética para realizar el menor gasto económico posible en su obtención. De igual modo, el sistema modela la cantidad de energía eléctrica suministrada a una serie de salidas, pues toda la energía generada debe ser consumida de uno u otro modo, como puede ser el consumo del hogar, carga de una batería, etc. Esto se traduce en una optimización y aprovechamiento de la energía, que además tiene como consecuencia un ahorro económico en la obtención de la energía necesaria. Para hacer esto posible se modela un problema de satisfacción de restricciones (PSR) cuyas soluciones son alcanzadas mediante programación lineal, haciendo uso de algoritmos de computación científica. Además, consta de una aplicación web que permite realizar simulaciones de optimizaciones diarias a sus usuarios, alojada en la nube de IBM Cloud Foundry y Amazon Web Services.

________________________________________________________________
# Trabajo Fin de Grado
### Título
Sistema Inteligente para la Gestión y Optimización de Energía Basado en la Nube
### Abstract
Energy consumption plays an essential role in the development and well-being of society. So much so that the energy demand multiplies over time and its price increases. Furthermore, fossil energy sources are exhaustible, we must opt for the use of renewable energies and self-consumption as much as possible. In order to manage this multitude of energy sources in the most efficient way, we have to take into account the factors conditioning them and select the most appropriate one at any moment to satisfy the energy demand. This final degree project is focused on the creation of an intelligent system so that homes' energy management is carried out in an optimal and efficient way through the incorporation of new energy sources such as the installation of photovoltaic modules and a battery. The installation is modeled as a Constraint Satisfaction Problem (CSP) identifying a set of variables, their domain and a set of restrictions between the variables values that are always determined by the installation configuration; by the physical properties of energy generation and consumption, as well as by climatic conditions. An objective energy cost function is added to this CSP, allowing the solution to be found orienting it to the aforementioned function minimization by means of linear programming. This allows to make the most of energy and results in a minimum economic home cost. This system can be used through a web application hosted in the IBM Cloud Foundry and Amazon Web Services that allows users to interact with it, configuring their home characteristics and being able to carry out simulations of a specific day. Thanks to the results of these simulations, users can compare the energy distribution and economic expense that would have been produced using the proposed system against what really happens with the electrical network exclusive consumption.
### Documentación
[Memoria TFG](https://github.com/pablopalomino96/TFG_PalominoGomez_Pablo/blob/doc/DOC/uclmTFGesi.pdf)
### Aplicación Web
[e-Optimizer](http://3.213.79.178:5000/)
### Acerca de
Este repositorio contiene el código y documentación del Trabajo Fin de Grado de Pablo Palomino Gómez, alumno de la Escuela Superior de Informática (Universidad de Castilla-La Mancha). El documento de este trabajo se distribuye con licencia Creative Commons Atribución Compartir Igual 4.0. El texto completo de la licencia puede obtenerse en https://creativecommons.org/licenses/by-sa/4.0/.
* **Autor** - Pablo Palomino Gómez
* **Director** - Luis Jiménez Linares
* **Director** - Luis Rodríguez Benítez
* **Intensificación** - Ciencias de la Computación




_______________________________________________________________________________
Sistema Inteligente para la Gestión y Optimización de Energía Basado en la Nube

© Pablo Palomino Gómez, 2019
