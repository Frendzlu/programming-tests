import csv
import time
from math import log, sin, cos, pi, sqrt
import pprint as pp

A = 2147483647


def generator_jed(n, seed=5, a=0, b=1):
	u0 = [seed / A]
	lm = lambda x: (x * 16807) % A
	rc = lambda x: x * (b - a) + a
	for i in range(n - 1):
		u0.append(lm(A * u0[i]) / A)
	return [rc(x) for x in u0]


def generator_kos(n, k=6, seed=5):
	X = generator_jed(n, seed=seed, a=1, b=k + 1)
	fl = lambda x: int(x) if x < k + 1 else k
	return [fl(x) for x in X]


def reduce(a):
	x = set()
	for el in a:
		x.add(el)
		if len(x) == 6:
			return sorted(list(x))
	raise ValueError


def generate(fn, save=True):
	studenty = []
	transf = lambda x: (x, reduce(generator_kos(20, 49, fn(x))[3:]))
	with open("studenty.csv", encoding="utf8") as f:
		reader = csv.reader(f, delimiter=';')
		next(reader)
		for row in reader:
			studenty.append(transf(int(row[5].split("@")[0])))
	x = set(["-".join([str(y) for y in x[1]]) for x in studenty])
	if len(x) != len(studenty):
		raise Exception("Got duplicate; please regenerate!")
	if save:
		with open("lotek.csv", "w", newline='') as f:
			writer = csv.writer(f, delimiter=';')
			writer.writerow(["Numer indeksu", "Numery do zaznaczenia"])
			for student in studenty:
				writer.writerow(student)
	return studenty


def intersection(listay, listb):
	return list(set(listay) & set(listb))


def save(array):
	with open("lotek.csv", "w", newline='') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(["SNumer indeksu", "Numery do zaznaczenia"])
		for student in array:
			writer.writerow(student)


def getStudentHitList(filename, chosenValues, checkIds, std, info={
	"showPerStudentInfo": True,
	"showCountStatistics": True,
	"showMonetaryStatistics": True
}, load=True):
	hits = {}
	studenty = std
	if load:
		with open(filename) as f:
			reader = csv.reader(f, delimiter=';')
			next(reader)
			for row in reader:
				studenty.append(row)
	counts = [0, 0, 0, 0, 0, 0]
	returnValue = 0
	netGain = 0
	if load:
		for (indeks, values) in studenty:
			values = values[1:-1].split(", ")
			corrects = len(intersection([int(x) for x in values], chosenValues))
			if corrects > 0:
				hits[indeks] = corrects
				counts[corrects - 1] += 1
	else:
		for value in studenty:
			corrects = len(intersection(value[1], chosenValues))
			if corrects > 0:
				hits[str(value[0])] = corrects
				counts[corrects - 1] += 1
	returnValue = 24 * counts[2] + 170 * counts[3] + 5300 * counts[4] + 2_000_000 * counts[5]
	netGain = returnValue - len(studenty) * 3
	hitlist = list(hits.items())
	hitlist.sort(key=lambda x: x[1], reverse=True)
	if info["showPerStudentInfo"]:
		for [i, v] in hitlist:
			print(f"{i}: {v} trafień")
	counts.reverse()
	if info["showCountStatistics"]:
		for id, val in enumerate(counts):
			if val > 0:
				print(f"{6 - id} of 6 digits have been marked correctly {val} times")
	if info["showMonetaryStatistics"]:
		print(f"Approximate winnings: {returnValue}")
		print(f"Net gain: {netGain}")
	for id in checkIds:
		if id in [int(x[0]) for x in hitlist]:
			print(f"{id} has guessed {hits[str(id)]} of 6 numbers correctly")
	return returnValue


lam = lambda x: int(x*time.time())
winnings = 0

LISTA = [21, 37, 42, 39, 17, 7, 2, 3, 5, 9, 1, 10, 22, 45]

std = []
attemptCounter = 1
failedGenerations = 0
highestSoFar = 0
while winnings < 10_000_000:
	# print("=" * 20, f"Attempt #{attemptCounter}", "=" * 20)
	try:
		std = generate(lam, False)
	except Exception:
		failedGenerations += 1
	winnings = getStudentHitList("lotek.csv", LISTA, [], std, {
		"showPerStudentInfo": False,
		"showCountStatistics": False,
		"showMonetaryStatistics": False
	}, False)
	if winnings > highestSoFar:
		highestSoFar = winnings
		print("=" * 20, f"Attempt #{attemptCounter}", "=" * 20)
		print(winnings)
	time.sleep(0.0001)
	attemptCounter += 1

save(std)
winnings = getStudentHitList("lotek.csv", LISTA, [421739, 419718, 421833, 419970], [], {
	"showPerStudentInfo": True,
	"showCountStatistics": True,
	"showMonetaryStatistics": True
})