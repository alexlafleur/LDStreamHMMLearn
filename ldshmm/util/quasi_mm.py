"""
This class is for generic quasiMMs. which are two-parameter families of mMMs.
"""
from nonstationary_mm import ConvexCombinationNSMM
from nonstationary_mm import NonstationaryMMClass


class QuasiMM(NonstationaryMMClass):
    def eval(self, taumeta, tauquasi):
        assert taumeta >= 1, "taumeta is not greater or equal 1"
        assert tauquasi >= 1, "tauquasi is not greater or equal 1"
        # return an MMM
        raise NotImplementedError("Please implement this method")

    def ismember(self, x) -> bool:
        raise NotImplementedError("Please implement this method")


class ConvexCombinationQuasiMM(QuasiMM):
    def __init__(self, smms, mu, timeendpoint='infinity'):
        # the spectral MM for mu = 0
        self.sMM0 = smms[0]
        # the spectral MM for mu = 1
        self.sMM1 = smms[1]
        # the weight function for the convex combination
        self.mu = mu
        # the upper endpoint of the temporal domain interval
        # may be a postive integer or the string 'infinity'
        self.timeendpoint = timeendpoint

    def eval(self, taumeta, tauquasi) -> ConvexCombinationNSMM:
        # return a non-stationary MM
        assert taumeta >= 1, "taumeta is not greater or equal 1"
        assert tauquasi >= 1, "tauquasi is not greater or equal 1"
        # scale the MMs according to the parameter taumeta
        # with the effect that the implied timescales are increased by a factor of taumeta
        smm0_scaled = self.sMM0.scale(taumeta)  # type sMM
        smm1_scaled = self.sMM1.scale(taumeta)  # type sMM

        # scale the independent variable of the weight function
        # by the product of taumeta and tauquasi
        # with the effect that the timescale of the weight function, which represents drift in the model
        # is increased by a factor of taumeta
        taudrift = taumeta * tauquasi

        def mu_scaled(t):
            return self.mu(t / taudrift)  # type function

        # scale the temporal domain by the drift scaling
        if self.timeendpoint is not 'infinity':
            timeendpoint_scaled = self.timeendpoint * taudrift
        else:
            timeendpoint_scaled = 'infinity'
        return ConvexCombinationNSMM(smm0_scaled, smm1_scaled, mu_scaled, timeendpoint_scaled)  # type nsMM

    def ismember(self, x) -> bool:
        raise NotImplementedError("Please implement this method")
