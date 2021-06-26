import os
import numpy as np
import matplotlib.pyplot as plt

scriptDir = os.path.dirname(os.path.realpath(__file__))


class edisim():

    def __init__(self, formData):
        self.simNum = int(formData['simNum'])
        self.spanNum = int(formData['spanNum'])
        self.faculty = int(formData['faculty'])
        self.ORG = int(formData['ORG'])
        self.URG = int(formData['URG'])
        self.orgApp = int(formData['orgApp'])
        self.minOrgScore = int(formData['minOrgScore'])
        self.maxOrgScore = int(formData['maxOrgScore'])
        self.urgApp_0 = int(formData['urgApp_0'])
        self.minUrgScore_0 = int(formData['minUrgScore_0'])
        self.maxUrgScore_0 = int(formData['maxUrgScore_0'])
        self.urgApp_1 = int(formData['urgApp_1'])
        self.minUrgScore_1 = int(formData['minUrgScore_1'])
        self.maxUrgScore_1 = int(formData['maxUrgScore_1'])

    # incentive function
    def booster(self, start, stop, num):
        """
        This function creates an array of random integers
        based on a starting point and a stoping point. The
        number of elements are set by the 'num' variable.
        """
        return np.random.randint(start, stop, num)

    # encoder function
    def encodeApplicant(self, listArray):
        """
        This function encodes a given list based on the weight of each
        elements. It returns a randomized array.
        """
        weight = np.array([], dtype=int)
        for kk in range(len(listArray)):
            weight = np.concatenate((weight,
                                    kk*np.ones(listArray[kk], dtype=int)))
            np.random.shuffle(weight)
        return weight

    def main(self, progBar):
        tORG = []
        tURG = []
        bestWins = 0    # number of best winners
        newORG = 0  # newly ORG hired
        newURG = 0  # newly URG hired

        for jj in range(self.simNum):
            progBar.setValue(jj)
            faculty = self.faculty
            ORG = self.ORG
            URG = self.URG
            bothGroups = np.array([self.URG, self.ORG], dtype=int)
            hires = 0    # number of hires
            retires = 0  # number of retires
            ratioORG = [ORG/faculty]    # ORG-faculty ratio
            ratioURG = [URG/faculty]    # URG-faculty ratio
            scores = []  # scores of hired

            for ii in range(self.spanNum):
                # ORG incentives
                qualityPointORG = self.booster(
                    self.minOrgScore, self.maxOrgScore, self.orgApp)

                # URG incentives
                if ii < 60:
                    qualityPointURG = self.booster(
                        self.minUrgScore_0, self.maxUrgScore_0, self.urgApp_0)
                elif ii >= 60:
                    qualityPointURG = self.booster(
                        self.minUrgScore_1, self.maxUrgScore_1, self.urgApp_1)

                # top applicants in normal EDI
                topORG_norm = sorted(qualityPointORG)[-2:]
                topURG_norm = sorted(qualityPointURG)[-2:]
                topPool = topORG_norm + topURG_norm

                # encoding top applicants
                w8topPool = self.encodeApplicant(topPool)
                # random pick form encoded list
                poolWinner = np.random.randint(0, len(w8topPool))

                # modeling hires
                # if top score of applicant is >= 90
                if topPool[w8topPool[poolWinner]] >= 90:
                    # if their encoding is 0 or 1
                    if w8topPool[poolWinner] == 0 or\
                            w8topPool[poolWinner] == 1:
                        ORG += 1     # add 1 to ORG population
                        hires += 1   # add 1 to hires
                        newORG += 1  # add 1 to newly ORG hired
                        # append applicant score to the list
                        scores.append(topPool[w8topPool[poolWinner]])
                        # if top score of applicant is 99
                        if topPool[w8topPool[poolWinner]] == 99:
                            bestWins += 1   # add 1 to best winner
                    else:
                        URG += 1     # add 1 to URG population
                        hires += 1   # add 1 to hires
                        newURG += 1  # add 1 to newly URG hired
                        # append applicant score to the list
                        scores.append(topPool[w8topPool[poolWinner]])

                # modeling attrition
                if ii % 4 == 0:  # loop if 1 year has passed
                    # encoding initial faculty members [10, 90]
                    w8faculty = self.encodeApplicant(bothGroups)
                    # random pick from encoded list
                    facultyLoser = np.random.randint(0, len(w8faculty))

                    if w8faculty[facultyLoser] == 1:    # if random pick is 1
                        ORG -= 1
                        retires += 1
                    else:   # if random pick is 0
                        URG -= 1
                        retires += 1

                ratioORG.append(ORG/(URG + ORG))
                ratioURG.append(URG/(URG + ORG))

            tORG.append(ratioORG)
            tURG.append(ratioURG)

        tORG = np.array(tORG)
        tURG = np.array(tURG)
        shapeORG = tORG.shape
        shapeURG = tURG.shape

        meanORG = []
        stdORG = []
        for hh in range(shapeORG[-1]):
            meanORG.append(tORG[:, hh].mean())
            stdORG.append(tORG[:, hh].std())

        meanURG = []
        stdURG = []
        for kk in range(shapeURG[-1]):
            meanURG.append(tURG[:, kk].mean())
            stdURG.append(tURG[:, kk].std())

        self.plotResults(meanURG, stdURG, 'URG')
        self.plotResults(meanORG, stdORG, 'ORG')

    def plotResults(self, y, stdError, name):
        plt.figure(figsize=(12, 8))
        plt.errorbar(np.arange(len(y)), y, yerr=stdError, label=name)
        plt.title('EDI Representation with Interventions')
        plt.xlabel('3-Month Intervals')
        plt.ylabel('EDI Representation')
        plt.legend()
        plt.show()
