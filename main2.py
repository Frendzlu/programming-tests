import csv
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


def generate():
	studenty = []
	transf = lambda x: (x, reduce(generator_kos(20, 49, x)[3:]))

	with open("studenty.csv", encoding="utf8") as f:
		reader = csv.reader(f, delimiter=';')
		next(reader)
		for row in reader:
			studenty.append(transf(int(row[5].split("@")[0])))
	x = set(["-".join([str(y) for y in x[1]]) for x in studenty])
	if len(x) != len(studenty):
		raise Exception("Got duplicate; please regenerate!")

	with open("lotek.csv", "w", newline='') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(["Numer indeksu", "Numery do zaznaczenia"])
		for student in studenty:
			writer.writerow(student)


def intersection(listay, listb):
	return list(set(listay) & set(listb))

# chosen values are the 6 from real life
def getStudentHitList(filename, chosenValues):
	hits = {}
	studenty = []
	with open(filename) as f:
		reader = csv.reader(f, delimiter=';')
		next(reader)
		for row in reader:
			studenty.append(row)
	counts = [0, 0, 0, 0, 0, 0]
	returnValue = 0
	netGain = 0
	for [indeks, values] in studenty:
		values = values[1:-1].split(", ")
		corrects = len(intersection([int(x) for x in values], chosenValues))
		if corrects > 0:
			hits[indeks] = corrects
			counts[corrects - 1] += 1
	returnValue = 24 * counts[2] + 170 * counts[3] + 5300 * counts[4] + 2_000_000 * counts[5]
	netGain = returnValue - len(studenty) * 3
	hits = {k: v for k, v in sorted(hits.items(), key=lambda item: item[1], reverse=True)}
	pp.pprint(hits)
	print(f"All six digits have been marked correctly {counts[5]} times")
	print(f"Five of six six digits have been marked correctly {counts[4]} times")
	print(f"Four of six digits have been marked correctly {counts[3]} times")
	print(f"Three of six digits have been marked correctly {counts[2]} times")
	print(f"Two of six digits have been marked correctly {counts[1]} times")
	print(f"One of six digits have been marked correctly {counts[0]} times")
	print(f"Approximate winnings: {returnValue}")
	print(f"Net gain: {netGain}")


# generate()
getStudentHitList("lotek.csv", [10, 18, 23, 36, 42, 46])
