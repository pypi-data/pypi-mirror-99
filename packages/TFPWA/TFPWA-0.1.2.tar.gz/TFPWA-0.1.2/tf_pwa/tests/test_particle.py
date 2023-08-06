import pytest

from tf_pwa.particle import *


def test_particle():
    a = BaseParticle("a", 1, -1)
    b = BaseParticle("b", 1, -1)
    c = BaseParticle("c", 0, -1)
    d = BaseParticle("d", 1, -1)
    tmp = BaseParticle("tmp", 1, -1)
    tmp2 = BaseParticle("tmp2", 1, -1)
    decay = Decay(a, [tmp, c])
    decay2 = Decay(tmp, [b, d])
    decay3 = Decay(a, [tmp2, d])
    decay4 = Decay(tmp2, [b, c])
    decaychain = DecayChain([decay, decay2])
    decaychain2 = DecayChain([decay3, decay4])
    decaygroup = DecayGroup([decaychain, decaychain2])
    print(decay.get_cg_matrix().T)
    print(np.array(decay.get_ls_list()))
    print(np.array(decay.get_ls_list())[:, 0])
    print(decaychain)
    print(decaychain.sorted_table())
    print(decaygroup)
    print(a.get_resonances())


def test_topology():
    a = BaseParticle("a")
    b = BaseParticle("B")
    c = BaseParticle("C")
    d = BaseParticle("D")
    r = BaseParticle("R")
    d1 = Decay(a, [r, c])
    d2 = Decay(r, [b, d])
    dec = DecayChain([d1, d2])
    print(dec.standard_topology())


def test_baseparticle():
    a = BaseParticle("a")
    assert str(a) == "a"
    b = BaseParticle("a:1")
    assert str(b) == "a:1"
    assert a.name == "a"
    c = BaseParticle("a", id_=1)
    assert str(c) == "a:1"
    assert a.name == "a"
    assert b == c
    assert a < c
    assert a < "a:1"
    assert c > a
    assert c > "a"


def test_basedecay():
    a = BaseParticle("a")
    b = BaseParticle("a:1")
    c = BaseParticle("c")
    d = BaseParticle("d")
    de = BaseDecay(c, [a, b])
    assert len(c.decay) == 1
    de2 = BaseDecay(d, [a, b], disable=True)
    assert len(c.decay) == 1
    c.remove_decay(de)
    assert len(c.decay) == 0
    de2 < de
    de2 > de
    assert de2 != de
    de2 > "s"
    de < "s"
    assert de != "s"


def test_sorted_table():
    a = {
        "a": ["b", "c", "d"],
        "r": ["c", "d"],
        "b": ["b"],
        "c": ["c"],
        "d": ["d"],
    }
    de = DecayChain.from_sorted_table(a)
    print(de.sorted_table_layers())
    b = {"a": ["b", "c", "d"], "b": ["b"], "c": ["c"], "d": ["d"]}
    de2 = DecayChain.from_sorted_table(b)
    print(de2.sorted_table_layers())
    c = {"a": ["b", "c", "d"], "c": ["c"], "d": ["d"]}
    with pytest.raises(Exception):
        de3 = DecayChain.from_sorted_table(c)


def test_depth_fisrt():
    decs = DecayChain.from_particles("a", ["B", "C", "D", "E"])
    for de in decs:
        used_node = [de.top]
        for i, dec in de.depth_first():
            assert dec.core in used_node
            for j in dec.outs:
                used_node.append(j)
        used_node = [de.top]
        for i, dec in list(de.depth_first(False))[::-1]:
            assert dec.core in used_node
            for j in dec.outs:
                used_node.append(j)
