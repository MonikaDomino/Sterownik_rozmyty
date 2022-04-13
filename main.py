import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Wejscia do systemu z zadeklarowana dziedzina

type_of_dirt = ctrl.Antecedent(np.arange(0, 100, 1), 'type_of_dirt')
degree_of_dirt = ctrl.Antecedent(np.arange(0, 100, 1), 'degree_of_dirt')
weight = ctrl.Antecedent(np.arange(0, 6, 1), 'weight')

# Wyjscie z systemu z zadeklarowana dziedzina

time = ctrl.Consequent(np.arange(0, 180, 1), 'time')
water_consumption = ctrl.Consequent(np.arange(0, 60, 1), 'water')
detergents = ctrl.Consequent(np.arange(0, 100, 1), 'detergents')
turnover = ctrl.Consequent(np.arange(0, 1200, 1), 'turnover')

# funkcje przynależności do zmiennej wejściowej

type_of_dirt['notGreasy'] = fuzz.trimf(type_of_dirt.universe, [5, 10, 25])
type_of_dirt['medium'] = fuzz.trimf(type_of_dirt.universe, [30, 50, 70])
type_of_dirt['greasy'] = fuzz.trimf(type_of_dirt.universe, [75, 90, 100])

degree_of_dirt['soft'] = fuzz.trimf(degree_of_dirt.universe, [5, 10, 25])
degree_of_dirt['medium'] = fuzz.trimf(degree_of_dirt.universe, [30, 50, 70])
degree_of_dirt['large'] = fuzz.trimf(degree_of_dirt.universe, [75, 90, 100])

weight['small'] = fuzz.trimf(weight.universe, [0, 1, 2])
weight['medium'] = fuzz.trimf(weight.universe, [2.5, 3, 4])
weight['large'] = fuzz.trimf(weight.universe, [4.5, 5, 6])


# funkcje przynależności do zmiennej wyjsciowej

time['VeryShort'] = fuzz.trimf(time.universe, [0, 10, 30])
time['Short'] = fuzz.trimf(time.universe, [15, 30, 50])
time['Medium'] = fuzz.trimf(time.universe, [40, 70, 80])
time['Long'] = fuzz.trimf(time.universe, [60, 100, 120])
time['VeryLong'] = fuzz.trimf(time.universe, [100, 140, 180])

water_consumption['Small'] = fuzz.trimf(water_consumption.universe, [0, 10, 25])
water_consumption['Medium'] = fuzz.trimf(water_consumption.universe, [18, 30, 45])
water_consumption['Large'] = fuzz.trimf(water_consumption.universe, [35, 50, 60])

detergents['Small'] = fuzz.trimf(detergents.universe, [0, 20, 45])
detergents['Medium'] = fuzz.trimf(detergents.universe, [35, 55, 65])
detergents['Large'] = fuzz.trimf(detergents.universe, [60, 80, 90])

turnover['low'] = fuzz.trimf(turnover.universe, [0, 100, 500])
turnover['average'] = fuzz.trimf(turnover.universe, [300, 550, 900])
turnover['high'] = fuzz.trimf(turnover.universe, [650, 875, 1200])

# Wizualizacja wejsc i wyjscia
# type_of_dirt.view()
# dirtness.view()
# detergents.view()
# weight.view()

# Baza wiedzy z regułami rozmytymi


rule1 = ctrl.Rule(degree_of_dirt['large'] | type_of_dirt['greasy'] | weight['large'], (time['VeryLong'],
                                                                                       water_consumption['Large'],
                                                                                       detergents['Large'],
                                                                                       turnover['high']))

rule11 = ctrl.Rule(degree_of_dirt['medium'] | type_of_dirt['greasy'] | weight['medium'], (time['Long'],
                                                                                          water_consumption['Large'],
                                                                                          detergents['Large'],
                                                                                          turnover['high']))

rule12 = ctrl.Rule(degree_of_dirt['soft'] | type_of_dirt['greasy'] | weight['small'], (time['Long'],
                                                                                       water_consumption['Large'],
                                                                                       detergents['Medium'],
                                                                                       turnover['high']))

rule2 = ctrl.Rule(degree_of_dirt['large'] | type_of_dirt['medium'] | weight['large'], (time['Long'],
                                                                                       water_consumption['Large'],
                                                                                       detergents['Medium'],
                                                                                       turnover['average']))

rule21 = ctrl.Rule(degree_of_dirt['medium'] | type_of_dirt['medium'] | weight['medium'], (time['Medium'],
                                                                                          water_consumption['Medium'],
                                                                                          detergents['Medium'],
                                                                                          turnover['average']))

rule22 = ctrl.Rule(degree_of_dirt['soft'] | type_of_dirt['medium'] | weight['small'], (time['Medium'],
                                                                                       water_consumption['Small'],
                                                                                       detergents['Medium'],
                                                                                       turnover['average']))

rule3 = ctrl.Rule(degree_of_dirt['large'] | type_of_dirt['notGreasy'] | weight['large'], (time['Medium'],
                                                                                          water_consumption['Medium'],
                                                                                          detergents['Small'],
                                                                                          turnover['low']))

rule31 = ctrl.Rule(degree_of_dirt['medium'] | type_of_dirt['notGreasy'] | weight['medium'], (time['Short'],
                                                                                             water_consumption[
                                                                                                 'Small'],
                                                                                             detergents['Small'],
                                                                                             turnover['low']))

rule32 = ctrl.Rule(degree_of_dirt['soft'] | type_of_dirt['notGreasy'] | weight['small'], (time['VeryShort'],
                                                                                          water_consumption['Small'],
                                                                                          detergents['Small'],
                                                                                          turnover['low']))


washing_ctrlWN = ctrl.ControlSystem([rule1, rule11, rule12, rule2, rule21, rule22, rule3, rule31, rule32])

# symulacja działania sterownika
washing_lctr_simulationWN = ctrl.ControlSystemSimulation(washing_ctrlWN)

# ustalamy wejście ostre (crisp)
washing_lctr_simulationWN.input['degree_of_dirt'] = 80
washing_lctr_simulationWN.input['type_of_dirt'] = 40
washing_lctr_simulationWN.input['weight'] = 5

# fuzzyfikacja wejścia ostrego - zamiana go na wejście rozmyte
# podstawienie rozmytego wejścia do reguł
# odczytanie z reguł rozmytego wyjścia
# defuzzyfikacja zmiennej wyjściowej
washing_lctr_simulationWN.compute()

time.view(sim=washing_lctr_simulationWN)
water_consumption.view(sim=washing_lctr_simulationWN)
turnover.view(sim=washing_lctr_simulationWN)
detergents.view(sim=washing_lctr_simulationWN)

plt.show()
