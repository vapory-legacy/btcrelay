from ethereum import tester

import pytest
slow = pytest.mark.slow

from utilRelay import dblSha256Flip, disablePyethLogging

disablePyethLogging()


class TestBtcTx(object):

    CONTRACT = 'example-btc-eth/btcTx.se'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        tester.gas_limit = 2 * 10**6
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed


    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    # @pytest.mark.skipif(True,reason='crash like crash604branch')
    def test_getOutputScriptWithMultipleInputs(self):
        # 3 ins, 2 outs
        rawTx = ("0100000003d64e15b7c11f7532059fe6aacc819b5d886e3aaa602078db57cbae2a8f17cde8000000006b483045022027a176130ebf8bf49fdac27cdc83266a68b19c292b08df1be29f3d964c7e90b602210084ae66b4ff5ed342d78102ef8a4bde87b3ded06929ccaf9a8f71b137baa1816a012102270d473b083897519e5f01c47de7ac50877b6a295775f35966922b3571614370ffffffff54f0e7ded00c01082257eda035d65513b509ddbbe05fae19df0065c294822c9d010000006c493046022100f7423fdbcff22d3cd49921d0af92420d548b925bb1671dc826f15ccc5e05c3de022100d60a6178d892bcf012a79cf9e3430ab70a33b3fa2d156ecf541584e44fa83b150121036674d9607e0461b158c4b3d6368d1869e893cd122c68ebe47af253ff686f064effffffffa6155f8b449da0d3f9d2e1bc8e864c8b78615c1fa560076acaee8802d256a6dd010000006c493046022100e220318b55597c80eecccf9b84f37ab287c14277ccccd269d32f863d8d58d403022100f87818cbed15276f0d5be51aed5bd3b8dea934d6dd2244f2c3170369b96f365501210204b08466f452bb42cefc081ca1c773e26ce0a43566bd9d17b30065c1847072f4ffffffff02301bb50e000000001976a914bdb644fddd802bf7388df220279a18abdf65ebb788ac009ccf6f000000001976a914802d61e8496ffc132cdad325c9abf2e7c9ef222b88ac00000000")
        outNum = 0
        expHashOfOutputScript = 56502271141207574289324577080259466406131090189524790551966501267826601078627
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1


    def test_2ndTxBlock100K(self):
        rawTx = "0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000"
        # rawTx = rawTx.decode('hex')
        outNum = 0

        # expHashOfOutputScript is by hashing the string (not binary), in this case it is:
        # >>> j
        # '76a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac'
        # >>> sha256(j)
        # '7d96f222c58c30cd5de7f083eb4c492b76d321f1d70f41bb29256a269e418512'
        # >>> 0x7d96f222c58c30cd5de7f083eb4c492b76d321f1d70f41bb29256a269e418512
        # 56805804292683358736007883811890392312689386233413306235613681413184995558674L
        expHashOfOutputScript = 56805804292683358736007883811890392312689386233413306235613681413184995558674
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1

    def test_getOutput0Script(self):
        # 1 ins, 1 outs
        rawTx = ("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
        outNum = 0
        expHashOfOutputScript = 15265305399265587892204941549768278966163359751228226364149342078721216369579
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1

    def test_getOutput1Script(self):
        # 1 ins, 1 outs
        rawTx = ("01000000016d5412cdc802cee86b4f939ed7fc77c158193ce744f1117b5c6b67a4d70c046b010000006c493046022100be69797cf5d784412b1258256eb657c191a04893479dfa2ae5c7f2088c7adbe0022100e6b000bd633b286ed1b9bc7682fe753d9fdad61fbe5da2a6e9444198e33a670f012102f0e17f9afb1dca5ab9058b7021ba9fcbedecf4fac0f1c9e0fd96c4fdc200c1c2ffffffff0245a87edb080000001976a9147d4e6d55e1dffb0df85f509343451d170d14755188ac60e31600000000001976a9143bc576e6960a9d45201ba5087e39224d0a05a07988ac00000000")
        outNum = 1
        expHashOfOutputScript = 115071730706014548547567659794968118611083380235397871058495281758347510448362
        res = self.c.doCheckOutputScript(rawTx, len(rawTx), outNum, expHashOfOutputScript)
        assert res == 1
