from visual_pygame_train import run
import random


# height_x(-), blockade_x(-), clear_x(+), flatness_x(+)
# pop[n][4]

def genetic_algorithm(fitness, n_pop, n_seeds):
    # initial population
    pop = []
    for _ in range(n_pop):
        # chromosome = []
        # for j in range(4):
        #     chromosome.append(random.uniform(-1, 1))
        chromosome = [0, random.uniform(-1, 0), 0, 1]
        pop.append(chromosome)
    # initial  best solution
    best = pop[0]

    # iterate through seeds
    seeds = range(100, n_seeds+100)
    for loop in range(1):  # loop n times though all seeds
        for seed in seeds:
            improved = False
            attempts = 1
            best_score = fitness(1, pop[0])
            print("==========  seed number: ", seed, "loop: ", loop+1, "  ==========")
            while not improved and attempts <= 5:
                scores = [fitness(seed, c) for c in pop]
                for j in range(n_pop):
                    if scores[j] > best_score:
                        best, best_score = pop[j], scores[j]
                        improved = True
                parents = [selection(pop, scores) for _ in range(n_pop)]
                children = []
                for j in range(0, n_pop, 2):
                    p1, p2 = parents[j], parents[j+1]
                    for c in crossover(p1, p2):
                        c = mutation(c, loop)
                        children.append(c)
                pop = children
                print("attempt: ", attempts)
                attempts += 1
            print("best: ", best)
            print("best score: ", best_score)
    return best  # [height_x(-), blockade_x(-), clear_x(+), flatness_x(+)]

    # # iterate through generations
    # for generation in range(n_gen):
    #     scores = [fitness(c) for c in pop]
    #     for i in range(n_pop):
    #         if scores[i] > best_score:
    #             best, best_score = pop[i], scores[i]
    #     parents = [selection(pop, scores) for _ in range(n_pop)]
    #     children = []
    #     for i in range(0, n_pop, 2):
    #         p1, p2 = parents[i], parents[i+1]
    #         for c in crossover(p1, p2):
    #             c = mutation(c)
    #             children.append(c)
    #     pop = children
    #     print("best: ", best)
    #     print("best score: ", best_score)
    # return best  # [height_x(-), blockade_x(-), clear_x(+), flatness_x(+)]


# returns the best among the k selected from population
def selection(pop, scores, k=3):
    x = random.randint(0, len(pop) - 1)
    best = pop[x]
    for i in range(k - 1):
        y = random.randint(0, len(pop) - 1)
        ind = pop[y]
        if scores[x] < scores[y]:
            best = ind
    return best


# crossover between parents to produce children
def crossover(p1, p2):
    pct = random.uniform(0.01, 0.99)
    c1, c2 = [0, 0, 0, 1], [0, 0, 0, 1]
    # for i in range(4):
    #     c1.append(p1[i] * pct + p2[i] * (1 - pct))
    #     c2.append(p1[i] * (1 - pct) + p2[i] * pct)
    c1[1] = p1[1] * pct + p2[1] * (1 - pct)
    c2[1] = p1[1] * (1 - pct) + p2[1] * pct
    return [c1, c2]


# 5% possibility that mutation happens
def mutation(children, n_loop):
    # for i in range(4):
    #     prob = random.random()
    #     if prob < 0.05:
    #         children[i] += random.uniform(-0.3 / (n_loop+1), 0.3 / (n_loop+1))
    prob = random.random()
    if prob < 0.05:
        children[1] += random.uniform(-0.1, 0.1)
    return children


if __name__ == "__main__":
    print(genetic_algorithm(run, 10, 20))
