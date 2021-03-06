# -*- coding: utf-8 -*-
from __future__ import print_function
from lmfdb.tests import LmfdbTest
import unittest2

from . import cmf_logger
cmf_logger.setLevel(100)


class CmfTest(LmfdbTest):
    def runTest():
        pass

    def test_expression_divides(self):
        # checks search of conductors dividing 1000
        self.check_args('/ModularForm/GL2/Q/holomorphic/?level_type=divides&level=1000&search_type=List', '40.2.k.a')

    def test_browse_page(self):
        r"""
        Check browsing for elliptic modular forms
        """
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/").get_data(as_text=True)
        assert '?search_type=Dimensions&dim=1' in data
        assert '?search_type=SpaceDimensions&char_order=1' in data
        assert "/stats" in data
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/?search_type=SpaceDimensions",follow_redirects=True).get_data(as_text=True)
        assert r'<a href="/ModularForm/GL2/Q/holomorphic/23/12/">229</a>' in data
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/?search_type=SpaceDimensions&char_order=1", follow_redirects=True).get_data(as_text=True)
        assert r'<a href="/ModularForm/GL2/Q/holomorphic/18/4/a/">1</a>' in data

    def test_stats(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/stats")
        assert "Classical modular forms: Statistics" in page.get_data(as_text=True)
        assert "Distribution" in page.get_data(as_text=True)
        assert "proportion" in page.get_data(as_text=True)
        assert "count" in page.get_data(as_text=True)
        assert "CM disc" in page.get_data(as_text=True)
        assert "RM disc" in page.get_data(as_text=True)
        assert "inner twists" in page.get_data(as_text=True)
        assert "projective image" in page.get_data(as_text=True)
        assert "character order" in page.get_data(as_text=True)

    def test_dynamic_stats(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/dynamic_stats?char_order=2&col1=level&buckets1=1-1000%2C1001-10000&proportions=recurse&col2=weight&buckets2=1-8%2C9-316&search_type=DynStats")
        data = page.get_data(as_text=True)
        for x in ["16576", "24174", "6172", "20.90%", "30.46%", "13.26%"]:
            assert x in data

    def test_sidebar(self):
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/Labels").get_data(as_text=True)
        assert 'Labels for classical modular forms' in data
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/Completeness").get_data(as_text=True)
        assert "Completeness of classical modular form data" in data
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/Reliability").get_data(as_text=True)
        assert "Reliability of classical modular form data" in data
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/Source").get_data(as_text=True)
        assert "Source of classical modular form data" in data

    def test_badp(self):
        data = self.tc.get("/ModularForm/GL2/Q/holomorphic/?level_primes=7&count=100&search_type=List").get_data(as_text=True)
        assert '273.1.o.a' in data
        assert '56.1.h.a' in data
        assert '14.2.a.a' in data
        assert '168' in data

    def test_level_bread(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1124/', follow_redirects = True)
        assert '1124.1.d.a' in page.get_data(as_text=True)
        assert r'\Q(\sqrt{-281})' in page.get_data(as_text=True)
        assert '1124.1.d.d' in page.get_data(as_text=True)
        assert r'\Q(\zeta_{20})^+' in page.get_data(as_text=True)
        assert '1124.1.ba.a' in page.get_data(as_text=True)
        assert r'\Q(\zeta_{35})' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1124/?weight=10&level=10', follow_redirects=True)
        assert 'Results (4 matches)'
        assert '10.10.b.a' in page.get_data(as_text=True)
        assert '2580' in page.get_data(as_text=True)

    @unittest2.skip("Long tests for many newform spaces, should be run & pass before any release")
    def test_many(self):
        from sage.all import ZZ, sqrt
        for Nk2 in range(1,2001):
            for N in ZZ(Nk2).divisors():
                    k = sqrt(Nk2/N)
                    if k in ZZ and k > 1:
                        print("testing (N, k) = (%s, %s)" % (N, k))
                        url  = "/ModularForm/GL2/Q/holomorphic/{0}/{1}/".format(N, k)
                        rv = self.tc.get(url,follow_redirects=True)
                        self.assertTrue(rv.status_code==200,"Request failed for {0}".format(url))
                        assert str(N) in rv.get_data(as_text=True)
                        assert str(k) in rv.get_data(as_text=True)
                        assert str(N)+'.'+str(k) in rv.get_data(as_text=True)

    def test_favorite(self):
        favorite_newform_labels = [
            [('23.1.b.a','Smallest analytic conductor'),
             ('11.2.a.a','First weight 2 form'),
             ('39.1.d.a','First D2 form'),
             ('7.3.b.a','First CM-form with weight at least 2'),
             ('23.2.a.a','First trivial-character non-rational form'),
             ('1.12.a.a','Delta'),
             ('124.1.i.a','First non-dihedral weight 1 form'),
             ('148.1.f.a','First S4 form'),
            ],
            [
                ('633.1.m.b','First A5 form'),
                ('163.3.b.a','Best q-expansion'),
                ('8.14.b.a','Large weight, non-self dual, analytic rank 1'),
                ('8.21.d.b','Large coefficient ring index'),
                ('3600.1.e.a','Many zeros in q-expansion'),
                ('983.2.c.a','Large dimension'),
                ('3997.1.cz.a','Largest projective image'),
                ('7524.2.l.b', 'CM-form by Q(-627) and many inner twists'),
            ]
        ]
        favorite_space_labels = [
            [('1161.1.i', 'Has A5, S4, D3 forms'),
             ('23.10', 'Mile high 11s'),
             ('3311.1.h', 'Most weight 1 forms'),
             ('1200.2.a', 'All forms rational'),
             ('9450.2.a','Most newforms'),
             ('4000.1.bf', 'Two large A5 forms'),
            ]
        ]
        for l in favorite_newform_labels:
            for elt, desc in l:
                page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?jump=%s" % elt, follow_redirects=True)
                assert ("Newform orbit %s" % elt) in page.get_data(as_text=True)
                # redirect to the same page
                page = self.tc.get("/ModularForm/GL2/Q/holomorphic/%s" % elt, follow_redirects=True)
                assert ("Newform orbit %s" % elt) in page.get_data(as_text=True)
        for l in favorite_space_labels:
            for elt, desc in l:
                page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?jump=%s" % elt, follow_redirects=True)
                assert elt in page.get_data(as_text=True)
                # redirect to the same page
                assert "Space of modular forms of " in page.get_data(as_text=True)
                page = self.tc.get("/ModularForm/GL2/Q/holomorphic/%s" % elt, follow_redirects=True)
                assert elt in page.get_data(as_text=True)
                assert "Space of modular forms of " in page.get_data(as_text=True)

    def test_tracehash(self):
        for t, l in [[1329751273693490116,'7.3.b.a'],[1294334189658968734, '4.5.b.a'],[0,'not found']]:
            page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?jump=%%23%d" % t, follow_redirects=True)
            assert l in page.get_data(as_text=True)

    def test_jump(self):
        for j, l in [['10','10.3.c.a'], ['3.6.1.a', '3.6.a.a'], ['55.3.d', '55.3.d'], ['55.3.54', '55.3.d'], ['20.5', '20.5'], ['yes','23.1.b.a'], ['yes&weight=2','11.2.a.a'], ['yes&weight=-2', 'There are no newforms specified by the query']]:
            page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?jump=%s" % j, follow_redirects=True)
            assert l in page.get_data(as_text=True)

    def test_failure(self):
        r"""
        Check that bad inputs are handled correctly
        """
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/983/2000/c/a/', follow_redirects=True)
        assert "Level and weight too large" in page.get_data(as_text=True)
        assert "for non trivial character." in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1000/4000/a/a/', follow_redirects=True)
        assert "Level and weight too large" in page.get_data(as_text=True)
        assert " for trivial character." in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/100/2/z/a/', follow_redirects=True)
        assert "Newform 100.2.z.a not found" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1000&weight=100-&search_type=List', follow_redirects=True)
        assert "No matches" in page.get_data(as_text=True)
        assert "Only for weight 1" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/maria/', follow_redirects=True)
        assert 'maria' in page.get_data(as_text=True) and "is not a valid newform" in page.get_data(as_text=True)

    def test_delta(self):
        r"""
        Check that the Delta function is ok....
        Recall that this version uses the old urls...
        """
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/1/12/")
        assert '1.12.a.a' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/1/12/a/")
        assert '1.12.a.a' in page.get_data(as_text=True)
        assert '16744' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/1/12/a/a/")
        assert '24q^{2}' in page.get_data(as_text=True)
        assert '84480q^{8}' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/1/12/a/a/?format=satake")
        assert '0.299367' in page.get_data(as_text=True)
        assert '0.954138' in page.get_data(as_text=True)
        page = self.tc.get('/L/ModularForm/GL2/Q/holomorphic/1/12/a/a/', follow_redirects=True)
        assert '0.792122' in page.get_data(as_text=True)

    def test_level11(self):
        r"""
        Check that the weight 2 form of level 11 works.
        """
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/11/2/a/a/")
        assert '2q^{2}' in page.get_data(as_text=True)
        assert '2q^{4}' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/11/2/a/a/?format=satake")
        assert r'0.707107' in page.get_data(as_text=True)
        assert r'0.957427' in page.get_data(as_text=True)
        assert r'0.223607' in page.get_data(as_text=True)
        assert r'0.974679' in page.get_data(as_text=True)
        ## We also check that the L-function works
        page = self.tc.get('/L/ModularForm/GL2/Q/holomorphic/11/2/a/a/', follow_redirects=True)
        assert '0.253841' in page.get_data(as_text=True)

    def test_triv_character(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/2/8/a/a/")
        assert r'1016q^{7}' in page.get_data(as_text=True)
        assert '1680' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/3/6/a/a/")
        assert '168q^{8}' in page.get_data(as_text=True)
        assert '36' in page.get_data(as_text=True)

    def test_non_triv_character(self):
        r"""
        Check that non-trivial characters are also working.
        """
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/13/2/e/a/")
        assert r'\Q(\sqrt{-3})' in page.get_data(as_text=True)
        assert '0.866025' in page.get_data(as_text=True)
        assert r'6q^{6}' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/10/4/b/a/")
        assert r'46q^{9}' in page.get_data(as_text=True)
        assert r'\Q(\sqrt{-1})' in page.get_data(as_text=True)
        assert r'10' in page.get_data(as_text=True)

    def test_get_args(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/13/10/a/")
        assert '11241' in page.get_data(as_text=True)
        assert '10099' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/13/10/1/",  follow_redirects=True)
        assert '11241' in page.get_data(as_text=True)
        assert '10099' in page.get_data(as_text=True)

    def test_empty(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/2/2/a/")
        assert 'The following table gives the dimensions of various' in page.get_data(as_text=True)
        assert 'subspaces' in page.get_data(as_text=True)
        assert r'\(M_{2}(\Gamma_0(2))\)' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/3/a/")
        assert 'weight is odd while the character is ' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/6/a/")
        for elt in ['Decomposition', r'S_{6}^{\mathrm{old}}(\Gamma_0(12))', 'lower level spaces']:
            assert elt in page.get_data(as_text=True)

    def test_not_in_db(self):
        # The following redirects to "ModularForm/GL2/Q/holomorphic/12000/12/"
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12000/12/")
        assert 'Space not in database' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12000/12/a/")
        assert 'Space 12000.12.a not found' in page.get_data(as_text=True)

    def test_character_validation(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/10/e/")
        assert 'Space 12.10.e not found' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/10/c/")
        assert 'since the weight is even while the character is' in page.get_data(as_text=True)

    def test_decomposition(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/6/12/", follow_redirects=True)
        assert r'Decomposition</a> of \(S_{12}^{\mathrm{new}}(\Gamma_1(6))\)' in page.get_data(as_text=True)
        page = self.tc.get('ModularForm/GL2/Q/holomorphic/38/9/')
        for elt in map(str,[378, 120, 258, 342, 120, 222, 36]):
            assert elt in page.get_data(as_text=True)
        for elt in ['38.9.b','38.9.d','38.9.f']:
            assert elt in page.get_data(as_text=True)
            assert elt + '.a' in page.get_data(as_text=True)
        for elt in ['Decomposition', r"S_{9}^{\mathrm{old}}(\Gamma_1(38))", "lower level spaces"]:
            assert elt in page.get_data(as_text=True)

    def test_convert_conreylabels(self):
        for c in [27, 31]:
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/38/9/%d/a/' % c,follow_redirects=True)
            assert "Newform orbit 38.9.d.a" in page.get_data(as_text=True)
            for e in range(1, 13):
                page = self.tc.get('/ModularForm/GL2/Q/holomorphic/38/9/d/a/%d/%d/' % (c, e),follow_redirects=True)
                assert "Newform orbit 38.9.d.a" in page.get_data(as_text=True)

    def test_dim_table(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?weight=12&level=23&search_type=Dimensions", follow_redirects=True)
        assert 'Dimension search results' in page.get_data(as_text=True)
        assert '229' in page.get_data(as_text=True) # Level 23, Weight 12

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?weight=12&level=1-100&search_type=Dimensions", follow_redirects=True)
        assert 'Dimension search results' in page.get_data(as_text=True)
        assert '229' in page.get_data(as_text=True) # Level 23, Weight 12

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?search_type=Dimensions", follow_redirects=True)
        assert 'Dimension search results' in page.get_data(as_text=True)
        assert '1-12' in page.get_data(as_text=True)
        assert '1-24' in page.get_data(as_text=True)
        assert '229' in page.get_data(as_text=True) # Level 23, Weight 12


        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-100&weight=1-20&search_type=Dimensions', follow_redirects=True)
        assert '253' in page.get_data(as_text=True) # Level 23, Weight 13
        assert '229' in page.get_data(as_text=True) # Level 23, Weight 12
        assert 'Dimension search results' in page.get_data(as_text=True)

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?level=3900-4100&weight=1-12&char_order=2-&search_type=Dimensions", follow_redirects=True)
        assert '426' in page.get_data(as_text=True) # Level 3999, Weight 1
        assert '128' in page.get_data(as_text=True) # Level 4000, Weight 1

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?level=3900-4100&weight=1-12&char_order=1&search_type=Dimensions", follow_redirects=True)
        assert 'Dimension search results' in page.get_data(as_text=True)
        assert '0' in page.get_data(as_text=True)

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?level=4002&weight=1&char_order=2-&search_type=Dimensions", follow_redirects=True)
        assert 'Dimension search results' in page.get_data(as_text=True)
        assert 'n/a' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=7,10&weight_parity=odd&char_parity=odd&count=50&search_type=Dimensions')
        for elt in map(str,[0,1,2,5,4,9,6,13,8,17,10]):
            assert elt in page.get_data(as_text=True)
        assert 'Dimension search results' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight_parity=odd&level=1-1000&weight=1-100&search_type=Dimensions')
        assert 'Error: Table too large: must have at most 10000 entries'

        #the other dim table
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/10/2/")
        assert '7' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/2/")
        for elt in map(str,[9,4,5]):
            assert elt in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/59/8/")
        for elt in map(str,[1044, 1042, 2, 986, 0, 58, 56]):
            assert elt in page.get_data(as_text=True)
        for etl in ['59.8.a', '59.8.a.a', '59.8.a.b', '59.8.c', '59.8.c.a']:
            assert elt in page.get_data(as_text=True)

    def test_character_parity(self):
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/10/c/")
        assert 'since the weight is even while the character is' in page.get_data(as_text=True)
        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/12/3/a/")
        assert 'since the weight is odd while the character is' in page.get_data(as_text=True)

    def test_dual(self):
        urls_set = [
                [('/ModularForm/GL2/Q/holomorphic/5/9/c/a/', 'Newform orbit 5.9.c.a'),
                ('/ModularForm/GL2/Q/holomorphic/5/9/c/a/2/1/', 'Dual form 5.9.c.a.2.1'),
                ('/ModularForm/GL2/Q/holomorphic/5/9/c/a/3/1/', 'Dual form 5.9.c.a.3.1'),
                ],
                [('/ModularForm/GL2/Q/holomorphic/5/9/c/a/', 'Newform orbit 5.9.c.a'),
                ('/ModularForm/GL2/Q/holomorphic/5/9/c/a/2/3/', 'Dual form 5.9.c.a.2.3'),
                ('/ModularForm/GL2/Q/holomorphic/5/9/c/a/3/3/', 'Dual form 5.9.c.a.3.3'),
                ],
                [
                ('/ModularForm/GL2/Q/holomorphic/13/2/e/a/', 'Newform orbit 13.2.e.a'),
                ('/ModularForm/GL2/Q/holomorphic/13/2/e/a/4/1/', 'Dual form 13.2.e.a.4.1'),
                ('/ModularForm/GL2/Q/holomorphic/13/2/e/a/10/1/', 'Dual form 13.2.e.a.10.1'),
                ]
                ]
        for urls in urls_set:
            for i, (url, _) in enumerate(urls):
                page = self.tc.get(url)
                for j, (other, name) in enumerate(urls):
                    if i != j:
                        assert other in page.get_data(as_text=True)
                        if i > 0:
                            assert name in page.get_data(as_text=True)

                if i > 0:
                    assert 'Embedding label' in page.get_data(as_text=True)
                    assert 'Root' in page.get_data(as_text=True)

    def test_embedded_invariants(self):
        for url in ['/ModularForm/GL2/Q/holomorphic/13/2/e/a/4/1/',
                    '/ModularForm/GL2/Q/holomorphic/13/2/e/a/10/1/']:

            page = self.tc.get(url)
            # root
            assert 'Root' in page.get_data(as_text=True)
            assert '0.500000' in page.get_data(as_text=True)
            assert '0.866025' in page.get_data(as_text=True)
            # p = 13
            for n in ['2.50000', '2.59808', '0.693375', '0.720577']:
                assert n in page.get_data(as_text=True)

            # p = 47
            for n in ['3.46410', '0.505291', '0.967559', '0.252646', '0.918699']:
                assert n in page.get_data(as_text=True)

            assert 'Newspace 13.2.e' in page.get_data(as_text=True)
            assert 'Newform orbit 13.2.e.a' in page.get_data(as_text=True)
            assert 'Dual form 13.2.e.a.' in page.get_data(as_text=True)
            assert 'L-function 13.2.e.a.' in page.get_data(as_text=True)

            assert '0.103805522628' in page.get_data(as_text=True)

            assert '13.2.e.a.4.1' in page.get_data(as_text=True)
            assert '13.2.e.a.10.1' in page.get_data(as_text=True)

    def test_satake(self):
        for url in ['/ModularForm/GL2/Q/holomorphic/11/2/a/a/?format=satake',
                '/ModularForm/GL2/Q/holomorphic/11/2/a/a/1/1/']:
            page = self.tc.get(url)
            assert r'0.707107' in page.get_data(as_text=True)
            assert r'0.957427' in page.get_data(as_text=True)
            assert r'0.223607' in page.get_data(as_text=True)
            assert r'0.974679' in page.get_data(as_text=True)
            assert r'0.288675' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/7/3/b/a/?&format=satake',
                '/ModularForm/GL2/Q/holomorphic/7/3/b/a/6/1/']:
            page = self.tc.get(url)
            assert r'0.750000' in page.get_data(as_text=True)
            assert r'0.661438' in page.get_data(as_text=True)
            assert r'0.272727' in page.get_data(as_text=True)
            assert r'0.962091' in page.get_data(as_text=True)
        assert r'1.00000' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/7/3/b/a/?&format=satake_angle',
                '/ModularForm/GL2/Q/holomorphic/7/3/b/a/6/1/']:
            page = self.tc.get(url)
            assert r'\(\pi\)' in page.get_data(as_text=True)
            assert r'\(0.769947\pi\)' in page.get_data(as_text=True)
            assert r'\(0.587926\pi\)' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/21/2/e/a/?format=satake',
                '/ModularForm/GL2/Q/holomorphic/21/2/e/a/4/1/',
                '/ModularForm/GL2/Q/holomorphic/21/2/e/a/16/1/',
                ]:
            page = self.tc.get(url)
            assert r'0.965926' in page.get_data(as_text=True)
            assert r'0.258819' in page.get_data(as_text=True)
            assert r'0.990338' in page.get_data(as_text=True)
            assert r'0.550990' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/5/9/c/a/?n=2-10&m=1-6&prec=6&format=satake',
                '/ModularForm/GL2/Q/holomorphic/5/9/c/a/2/1/',
                '/ModularForm/GL2/Q/holomorphic/5/9/c/a/3/1/',
                ]:
            page = self.tc.get(url)
            assert '0.972878' in page.get_data(as_text=True)
            assert '0.231320' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/5/9/c/a/?n=2-10&m=1-6&prec=6&format=satake',
                '/ModularForm/GL2/Q/holomorphic/5/9/c/a/2/3/',
                '/ModularForm/GL2/Q/holomorphic/5/9/c/a/3/3/',
                ]:
            page = self.tc.get(url)
            assert '0.00593626' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/31/2/c/a/?m=1-4&n=2-10&prec=6&format=satake',
                '/ModularForm/GL2/Q/holomorphic/31/2/c/a/5/1/',
                '/ModularForm/GL2/Q/holomorphic/31/2/c/a/25/1/',
                ]:
            page = self.tc.get(url)
            assert '0.998759' in page.get_data(as_text=True)
            assert '0.0498090' in page.get_data(as_text=True)
            assert '0.542515' in page.get_data(as_text=True)
            assert '0.840046' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/31/2/c/a/?m=1-4&n=2-10&prec=6&format=satake_angle',
                '/ModularForm/GL2/Q/holomorphic/31/2/c/a/5/1/',
                '/ModularForm/GL2/Q/holomorphic/31/2/c/a/25/1/',
                ]:
            page = self.tc.get(url)
            assert r'0.984139\pi' in page.get_data(as_text=True)
            assert r'0.317472\pi' in page.get_data(as_text=True)


        #test large floats
        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/1/']:
            page = self.tc.get(url)
            assert '213.765' in page.get_data(as_text=True)
            assert '5.39613e49' in page.get_data(as_text=True)
            assert '7.61562e49' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/2/']:
            page = self.tc.get(url)
            assert '3412.77' in page.get_data(as_text=True)
            assert '1.55372e49' in page.get_data(as_text=True)
            assert '1.00032e49' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/3/']:
            page = self.tc.get(url)
            assert '3626.53' in page.get_data(as_text=True)
            assert '1.17540e49' in page.get_data(as_text=True)
            assert '1.20001e50' in page.get_data(as_text=True)

        # same numbers but normalized
        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=analytic_embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/1/']:
            page = self.tc.get(url)
            assert '0.993913' in page.get_data(as_text=True)
            assert '1.36787' in page.get_data(as_text=True)

        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=analytic_embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/2/']:
            page = self.tc.get(url)
            assert '0.286180' in page.get_data(as_text=True)
            assert '0.179671' in page.get_data(as_text=True)
        for url in ['/ModularForm/GL2/Q/holomorphic/1/36/a/a/?m=1-3&n=695-696&prec=6&format=analytic_embed',
                    '/ModularForm/GL2/Q/holomorphic/1/36/a/a/1/3/']:
            page = self.tc.get(url)
            assert '0.216496' in page.get_data(as_text=True)
            assert '2.15537' in page.get_data(as_text=True)

        # test some exact values
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/25/2/e/a/?n=97&m=8&prec=6&format=satake_angle')
        assert '0.0890699' in page.get_data(as_text=True)
        assert '0.689070' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/25/2/d/a/?m=4&n=97&prec=6&format=satake_angle')
        assert '0.237314' in page.get_data(as_text=True)
        assert '0.637314' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/210/2/a/a/?format=satake&n=2-20')
        # alpha_11
        assert '0.603023' in page.get_data(as_text=True)
        assert '0.797724' in page.get_data(as_text=True)
        # alpha_13
        assert '0.277350' in page.get_data(as_text=True)
        assert '0.960769' in page.get_data(as_text=True)
        # alpha_17
        assert '0.727607' in page.get_data(as_text=True)
        assert '0.685994' in page.get_data(as_text=True)

        # specifying embeddings
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/99/2/p/a/?n=2-10&m=2.1%2C+95.10&prec=6&format=embed')
        for elt in ['2.1','95.10','1.05074','0.946093', '2.90568', '0.305399']:
            assert elt in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/13/2/e/a/?m=1-2&n=2-10000&prec=6&format=embed')
        assert "Only" in page.get_data(as_text=True)
        assert "up to 1000 are available" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/7524/2/l/b/?n=5000&m=&prec=&format=embed')
        assert "Only" in page.get_data(as_text=True)
        assert "up to 3000 are available" in page.get_data(as_text=True)
        assert "in specified range; resetting to default" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/7524/2/l/b/?n=1500-4000&m=&prec=&format=embed')
        assert "Only" in page.get_data(as_text=True)
        assert "up to 3000 are available" in page.get_data(as_text=True)
        assert "limiting to" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/13/2/e/a/?m=1-2&n=3.5&prec=6&format=embed')
        assert "must be an integer, range of integers or comma separated list of integers" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/419/3/h/a/?n=2-10&m=1-20000&prec=6&format=embed', follow_redirects=True)
        assert "Web interface only supports 1000 embeddings at a time.  Use download link to get more (may take some time)." in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/419/3/h/a/?n=3.14&format=embed', follow_redirects=True)
        assert "must be an integer, range of integers or comma separated list of integers" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/99/2/p/a/?n=2-10&m=1-20&prec=16&format=embed')
        assert 'must be a positive integer, at most 15 (for higher precision, use the download button)' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/99/2/p/a/?n=999-1001&m=1-20&prec=6&format=embed')
        assert 'Only' in page.get_data(as_text=True)
        assert 'up to 1000 are available' in page.get_data(as_text=True)
        assert 'a_{1000}' in page.get_data(as_text=True)

    def test_download_qexp(self):
        for label, exp in [
                ['11.7.b.a'
                    , '[0, 10, 64]'],
                ['11.2.a.a'
                    , '[-2, -1, 2]'],
                ['21.2.g.a'
                    , '[0, -a - 1, 2*a - 2]'],
                ['59.2.a.a'
                    , '[-a^4 + 7*a^2 + 3*a - 5, a^4 - a^3 - 6*a^2 + 2*a + 3, a^3 - a^2 - 4*a + 3]'],
                ['13.2.e.a'
                    , '[-a - 1, 2*a - 2, a]'],
                ['340.1.ba.b'
                    , '[z, 0, z^2]'],
                ['24.3.h.a'
                    , '[-2, 3, 4]'],
                ['24.3.h.c'
                    , '[a, -1/4*a^3 - a^2 - 1/2*a - 3, a^2]'],
                ]:
            sage_code = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_qexp/%s' % label, follow_redirects=True).get_data(as_text=True)
            assert "make_data" in sage_code
            assert "aps_data" in sage_code
            sage_code += "\n\nout = str(make_data().list()[2:5])\n"
            exec(sage_code, globals())
            global out
            assert str(out) == exp
        for label in ['212.2.k.a', '887.2.a.b']:
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_qexp/{}'.format(label), follow_redirects=True)
            assert 'No q-expansion found for {}'.format(label) in page.get_data(as_text=True)

    def test_download(self):
        r"""
        Test download function
        """

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/23.10', follow_redirects=True)
        assert '[0, 187, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, 969023, -478731' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/1161.1.i', follow_redirects=True)
        assert '[0, 14, 0, 0, -2, 0, 0, 0, 0, 0, -2, 0, 0, 1, 0, 0, -10, 0, 0, 1, 0, 0' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/1161.1.i.maria.josefina', follow_redirects=True)
        assert 'Invalid label' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/4021.2.mz', follow_redirects=True)
        assert 'Label not found:'
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/4021.2.c', follow_redirects=True)
        assert 'We have not computed traces for' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_traces/27.2.e.a', follow_redirects=True)
        assert '[0, 12, -6, -6, -6, -3, 0, -6, 6, 0, -3, 3, 12, -6, 15, 9, 0, 9, 9, -3, -3, -12, 3, -12, -18, 3, -30' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_newform/27.2.e.a', follow_redirects=True)
        assert '"analytic_rank_proved": true' in page.get_data(as_text=True)
        assert '[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]' in page.get_data(as_text=True) # a1 (make sure qexp is there)
        assert '[1, 1, 27, 5, 1, 9, 0]' in page.get_data(as_text=True) # non-trivial inner twist
        assert '[0, 12, -6, -6, -6, -3, 0, -6, 6, 0, -3, 3, 12, -6, 15, 9, 0, 9, 9, -3, -3, -12, 3, -12, -18, 3, -30' in page.get_data(as_text=True)
        assert '1.2.3.c9' in page.get_data(as_text=True) # Sato-Tate group

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_full_space/20.5', follow_redirects = True)
        assert r"""["20.5.b.a", "20.5.d.a", "20.5.d.b", "20.5.d.c", "20.5.f.a"]""" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_newspace/244.4.w')
        assert "[7, 31, 35, 43, 51, 55, 59, 63, 67, 71, 79, 87, 91, 115, 139, 227]" in page.get_data(as_text=True)
        assert "244.4.w" in page.get_data(as_text=True)

    def test_download_magma(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_newform_to_magma/23.1.b.a.z')
        assert 'Label not found' in page.get_data(as_text=True)

        # test MakeNewformModFrm
        for label, expected in [
                ['11.2.a.a',
                    'q - 2*q^2 - q^3 + 2*q^4 + q^5 + 2*q^6 - 2*q^7 - 2*q^9 - 2*q^10 + q^11 + O(q^12)'],
                ['21.2.g.a',
                    'q + (-nu - 1)*q^3 + (2*nu - 2)*q^4 + (-3*nu + 2)*q^7 + 3*nu*q^9 + O(q^12)'],
                ['59.2.a.a',
                    'q + (-nu^4 + 7*nu^2 + 3*nu - 5)*q^2 + (nu^4 - nu^3 - 6*nu^2 + 2*nu + 3)*q^3 + (nu^3 - nu^2 - 4*nu + 3)*q^4 + (nu^4 - 6*nu^2 - 4*nu + 3)*q^5 + (-3*nu^4 + 2*nu^3 + 17*nu^2 - 3*nu - 7)*q^6 + (-nu^2 + 3)*q^7 + (3*nu^4 - 2*nu^3 - 17*nu^2 + 3*nu + 5)*q^8 + (2*nu^4 - 13*nu^2 - 4*nu + 8)*q^9 + (3*nu^4 - 2*nu^3 - 17*nu^2 + nu + 5)*q^10 + (-4*nu^4 + 2*nu^3 + 24*nu^2 + 2*nu - 12)*q^11 + O(q^12)'],
                ['13.2.e.a',
                    'q + (-nu - 1)*q^2 + (2*nu - 2)*q^3 + nu*q^4 + (-2*nu + 1)*q^5 + (-2*nu + 4)*q^6 + (2*nu - 1)*q^8 - nu*q^9 + (3*nu - 3)*q^10 + O(q^12)'],
                ['340.1.ba.b',
                    'q + zeta_8*q^2 + zeta_8^2*q^4 - zeta_8^3*q^5 + zeta_8^3*q^8 - zeta_8*q^9 + q^10 + O(q^12)'],
                ['24.3.h.a',
                    'q - 2*q^2 + 3*q^3 + 4*q^4 + 2*q^5 - 6*q^6 - 10*q^7 - 8*q^8 + 9*q^9 - 4*q^10 - 10*q^11 + O(q^12)'],
                ['24.3.h.c',
                    'q + nu*q^2 + 1/4*(-nu^3 - 4*nu^2 - 2*nu - 12)*q^3 + nu^2*q^4 + (nu^3 + 2*nu)*q^5 + (-nu^3 + nu^2 - 3*nu + 4)*q^6 + 4*q^7 + nu^3*q^8 + 1/2*(-nu^3 - 10*nu - 10)*q^9 + (-4*nu^2 - 16)*q^10 + 1/2*(-3*nu^3 - 6*nu)*q^11 + O(q^12)'],
                ]:
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_newform_to_magma/%s' % label)
            makenewform = 'MakeNewformModFrm_%s_%s_%s_%s' % tuple(label.split('.'))
            assert makenewform  in page.get_data(as_text=True)
            magma_code = page.get_data(as_text=True) + '\n' + '%s();\n' % makenewform
            self.assert_if_magma(expected, magma_code, mode='equal')

        for label, expected in [['24.3.h.a',
                    'Modular symbols space of level 24, weight 3, character Kronecker character -24, and dimension 1 over Rational Field'],
                ['24.3.h.c',
                    'Modular symbols space of level 24, weight 3, character Kronecker character -24, and dimension 4 over Rational Field'],
                ['54.2.e.a',
                    'Modular symbols space of level 54, weight 2, character $.1^16, and dimension 1 over Cyclotomic Field of order 9 and degree 6'],
                ['54.2.e.b',
                    'Modular symbols space of level 54, weight 2, character $.1^16, and dimension 2 over Cyclotomic Field of order 9 and degree 6'
                    ],
                ['212.2.k.a',
                    'Modular symbols space of level 212, weight 2, character $.1*$.2^17, and dimension 1 over Cyclotomic Field of order 52 and degree 24'
                    ]
                ]:
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/download_newform_to_magma/%s' % label)
            makenewform = 'MakeNewformModSym_%s_%s_%s_%s' % tuple(label.split('.'))
            assert makenewform  in page.get_data(as_text=True)
            magma_code = page.get_data(as_text=True) + '\n' + '%s();\n' % makenewform
            self.assert_if_magma(expected, magma_code, mode='equal')

    def test_expression_level(self):
        # checks we can search on 2*7^2
        self.check_args('/ModularForm/GL2/Q/holomorphic/?hst=List&level=2*7%5E2&search_type=List', '98.2.a.a')

    def test_download_search(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?Submit=sage&download=1&query=%7B%27level_radical%27%3A+5%2C+%27dim%27%3A+%7B%27%24lte%27%3A+10%2C+%27%24gte%27%3A+1%7D%2C+%27weight%27%3A+10%7D&search_type=Traces', follow_redirects = True)
        assert '5.10.a.a' in page.get_data(as_text=True)
        assert '1, -8, -114, -448, -625, 912, 4242, 7680, -6687, 5000, -46208, 51072, -115934, -33936' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?Submit=sage&download=1&query=%7B%27level_radical%27%3A+5%2C+%27dim%27%3A+%7B%27%24lte%27%3A+10%2C+%27%24gte%27%3A+1%7D%2C+%27weight%27%3A+10%7D&search_type=List', follow_redirects = True)
        assert '5.10.a.a' in page.get_data(as_text=True)
        assert ('[5, 10, 1, 2.5751791808193656, [0, 1], "1.1.1.1", [], [], [-8, -114, -625, 4242]]' in page.get_data(as_text=True)) or ('[5, 10, 1, 2.57517918082, [0, 1], "1.1.1.1", [], [], [-8, -114, -625, 4242]]' in page.get_data(as_text=True)) # Different tests for py2 and py3 due to different number of digits being returned.

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?Submit=gp&download=1&query=%7B%27num_forms%27%3A+%7B%27%24gte%27%3A+1%7D%2C+%27weight%27%3A+5%2C+%27level%27%3A+20%7D&search_type=Spaces')
        for elt in ["20.5.b", "20.5.d", "20.5.f"]:
            assert elt in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?Submit=sage&download=1&query=%7B%27dim%27%3A+%7B%27%24gte%27%3A+2000%7D%2C+%27num_forms%27%3A+%7B%27%24exists%27%3A+True%7D%7D&search_type=SpaceTraces', follow_redirects=True)
        assert 'Error: We limit downloads of traces to' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?Submit=sage&download=1&query=%7B%27dim%27%3A+%7B%27%24gte%27%3A+30000%7D%2C+%27num_forms%27%3A+%7B%27%24exists%27%3A+True%7D%7D&search_type=SpaceTraces', follow_redirects=True)
        assert '863.2.c' in page.get_data(as_text=True)

    def test_random(self):
        r"""
        Test that we don't hit any error on a random newform
        """
        def check(page):
            assert 'Newspace' in page.get_data(as_text=True), page.url
            assert 'parameters' in page.get_data(as_text=True), page.url
            assert 'Properties' in page.get_data(as_text=True), page.url
            assert 'Newform' in page.get_data(as_text=True), page.url
            assert 'expansion' in page.get_data(as_text=True), page.url
        for i in range(100):
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/random', follow_redirects = True)
            check(page)

        for w in ('1', '2', '3', '4', '5', '6-10', '11-20', '21-40', '41-'):
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight=%s&search_type=Random' % w, follow_redirects = True)
            check(page)
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/random?weight=%s' % w, follow_redirects = True)
            check(page)

        for l in ('1', '2-100', '101-500', '501-1000', '1001-2000', '2001-'):
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=%s&search_type=Random' % l, follow_redirects = True)
            check(page)
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/random?level=%s' % l, follow_redirects = True)
            check(page)

    def test_dimension(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=10&weight=1-14&dim=1&search_type=List', follow_redirects = True)
        assert "14 matches" in page.get_data(as_text=True)
        assert 'A-L signs' in page.get_data(as_text=True)

    def test_traces(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=244&weight=4&count=50&search_type=Traces', follow_redirects = True)
        assert "Results (18 matches)" in page.get_data(as_text=True)
        for elt in map(str,[-98,-347,739,0,147,-414,324,306,-144,0,24,-204,153,414,-344,-756,-24,164]):
            assert elt in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=244&weight=4&search_type=Traces&n=1-40&n_primality=prime_powers&an_constraints=a3%3D0%2Ca37%3D0', follow_redirects = True)
        assert "Results (3 matches)" in page.get_data(as_text=True)
        for elt in map(str,[-6,-68, 3224, 206, 4240, -408, -598, 1058]):
            assert elt in page.get_data(as_text=True)

        page = self.tc.get("/ModularForm/GL2/Q/holomorphic/?weight_parity=odd&level=7&weight=7&search_type=Traces&n=1-10&n_primality=all")
        assert "Results (4 matches)" in page.get_data(as_text=True)
        for elt in map(str,[17,0,-80,60,3780,-1200]):
            assert elt in page.get_data(as_text=True)

    def test_trivial_searches(self):
        from sage.all import Subsets
        for begin in [
                ('level=10&weight=1-20&dim=1',
                    ['Results (21 matches)', '171901114', 'No', '10.723', 'A-L signs']
                    ),
                ('level=10%2C13%2C17&weight=1-8&dim=1',
                    ['Results (12 matches)', '1373', 'No', '0.136']
                    )]:
            for s in Subsets(['has_self_twist=no', 'is_self_dual=yes', 'nf_label=1.1.1.1','char_order=1','inner_twist_count=1']):
                s = '&'.join(['/ModularForm/GL2/Q/holomorphic/?search_type=List', begin[0]] + list(s))
                page = self.tc.get(s,  follow_redirects=True)
                for elt in begin[1]:
                    assert elt in page.get_data(as_text=True), s

        for begin in [
                ('level=1-330&weight=1&projective_image=D2',
                    ['Results (49 matches)',
                        '328.1.c.a', r"\sqrt{-82}", r"\sqrt{-323}", r"\sqrt{109}"]
                    ),
                ('level=900-1000&weight=1-&projective_image=D2',
                    ['Results (26 matches)', r"\sqrt{-1}", r"\sqrt{-995}", r"\sqrt{137}"]
                    )]:
            for s in Subsets(['has_self_twist=yes', 'has_self_twist=cm', 'has_self_twist=rm',  'projective_image_type=Dn','dim=1-4']):
                s = '&'.join(['/ModularForm/GL2/Q/holomorphic/?search_type=List', begin[0]] + list(s))
                page = self.tc.get(s,  follow_redirects=True)
                for elt in begin[1]:
                    assert elt in page.get_data(as_text=True), s

    def test_parity(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight_parity=even&char_parity=even&search_type=List')
        assert '11.2.a.a' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight_parity=odd&char_parity=odd&search_type=List')
        assert '23.1.b.a' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight_parity=even&char_parity=even&weight=3&search_type=List')
        assert "No matches" in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?weight_parity=even&char_parity=odd&search_type=List')

    def test_coefficient_fields(self):
        r"""
        Test the display of coefficient fields.
        """
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/9/8/a/')
        assert r'\Q(\sqrt{10})' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/11/6/a/')
        assert '3.3.54492.1' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/27/2/e/a/')
        assert '12.0.1952986685049.1' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-500&weight=2&nf_label=16.0.1048576000000000000.1&prime_quantifier=subsets&search_type=List')
        assert r'\zeta_{40}' in page.get_data(as_text=True)
        assert "Results (6 matches)" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-4000&weight=1&nf_label=9.9.16983563041.1&prime_quantifier=subsets&projective_image=D19&search_type=List')
        assert r"Q(\zeta_{38})^+" in page.get_data(as_text=True)
        assert "Results (32 matches)"

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-100&weight=2&dim=4&nf_label=4.0.576.2&prime_quantifier=subsets&search_type=List')
        assert 'Results (7 matches)' in page.get_data(as_text=True)
        assert r'\Q(\sqrt{2}, \sqrt{-3})' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?dim=8&char_order=20&cm=no&rm=no&search_type=List')
        assert "Results (17 matches)" in page.get_data(as_text=True)
        assert r"Q(\zeta_{20})" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-4000&weight=1&dim=116&search_type=List')
        assert "Results (displaying both matches)" in page.get_data(as_text=True)
        assert r"Q(\zeta_{177})" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-100&weight=2&dim=4&nf_label=4.0.576.2&prime_quantifier=subsets')
        assert 'Results (7 matches)' in page.get_data(as_text=True)
        assert r'\Q(\sqrt{2}, \sqrt{-3})' in page.get_data(as_text=True)

    def test_inner_twist(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/3992/1/ba/a/')
        assert "499.g" in page.get_data(as_text=True)
        assert "3992.ba" in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/190/2/i/a/')
        for elt in ['5.b', '19.c', '95.i']:
            assert elt in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1816/1/l/a/')
        for elt in ['227.c','1816.l']:
            assert elt in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/2955/1/c/e/')
        for elt in ['3.b','5.b','197.b','2955.c']:
            assert elt in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/52/18/a/a/')
        assert "This newform does not admit any (" in page.get_data(as_text=True)
        assert "nontrivial" in page.get_data(as_text=True)
        assert "inner twist" in page.get_data(as_text=True)

    def test_self_twist(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/2955/1/c/e/')
        for elt in [r'\Q(\sqrt{-591})', r'\Q(\sqrt{-15})', r'\Q(\sqrt{985})']:
            assert elt in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1124/1/d/a/')
        for elt in [r'\Q(\sqrt{-281})', r'\Q(\sqrt{-1})', r'\Q(\sqrt{281})']:
            assert elt in page.get_data(as_text=True)

    def test_selft_twist_disc(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-40&weight=1-6&self_twist_discs=-3&search_type=List')
        for elt in [r'\Q(\sqrt{-39})', r'\Q(\sqrt{-3})']:
            assert elt in page.get_data(as_text=True)
        assert 'Results (22 matches)' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-100&self_twist_discs=5&search_type=List')
        for elt in [-55,-11,5,-5,-1,-95,-19]:
            assert (r'\Q(\sqrt{%d})' % elt) in page.get_data(as_text=True)
        assert 'Results (3 matches)' in page.get_data(as_text=True)
        for d in [3,-5]:
            page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=1-100&self_twist_discs=%d&search_type=List' % d)
            assert 'is not a valid input for' in page.get_data(as_text=True)

    def test_projective(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/2955/1/c/e/')
        assert 'D_{2}' in page.get_data(as_text=True)
        assert r'\Q(\sqrt{-15}, \sqrt{-591})' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1124/1/d/a/')
        assert 'D_{2}' in page.get_data(as_text=True)
        assert r'\Q(i, \sqrt{281})' in page.get_data(as_text=True)

    def test_artin(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/2955/1/c/e/')
        assert 'Artin representation 2.3_5_197.8t11.1' in page.get_data(as_text=True)
        assert 'D_4:C_2' in page.get_data(as_text=True)
        assert '8.0.1964705625.1' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/1124/1/d/a/')
        assert 'Artin representation 2.2e2_281.4t3.2' in page.get_data(as_text=True)
        assert '4.0.4496.1' in page.get_data(as_text=True)
        assert 'D_4' in page.get_data(as_text=True)

        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/124/1/i/a/67/1/')
        assert 'Artin representation 2.2e2_31.16t60.1c3' in page.get_data(as_text=True)
        assert 'SL(2,3):C_2' in page.get_data(as_text=True)
        assert '4.0.15376.1' in page.get_data(as_text=True)

    def test_AL_search(self):
        r"""
        Test that we display AL eigenvals/signs
        """
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=15&char_order=1&search_type=List', follow_redirects=True)
        assert 'A-L signs' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=15&search_type=Spaces', follow_redirects=True)
        assert 'AL-dims.' in page.get_data(as_text=True)
        assert r'\(0\)+\(1\)+\(0\)+\(0\)' in page.get_data(as_text=True)

    def test_Fricke_signs_search(self):
        r"""
        Test that we display Fricke signs
        """
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?level=15%2C20&weight=2&dim=1&search_type=List',  follow_redirects=True)
        assert 'Fricke sign' in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?char_order=1&search_type=List',  follow_redirects=True)
        assert 'Fricke sign' in page.get_data(as_text=True)

    def displaying_weight1_search(self):
        for typ in ['List', 'Traces', 'Dimensions']:
            for search in ['weight=1', 'rm_discs=5','has_self_twist=rm','cm_discs=-3%2C+-39']:
                page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?%s&search_type=%s' % (search, typ),  follow_redirects=True)
                assert 'Only for weight 1:' in page.get_data(as_text=True)

    def test_is_self_dual(self):
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?is_self_dual=yes&search_type=List' ,  follow_redirects=True)
        for elt in ['23.1.b.a', '31.1.b.a', '111.1.d.a']:
            assert elt in page.get_data(as_text=True)
        page = self.tc.get('/ModularForm/GL2/Q/holomorphic/?is_self_dual=no&search_type=List',  follow_redirects=True)
        for elt in ['52.1.j.a', '57.1.h.a', '111.1.h.a']:
            assert elt in page.get_data(as_text=True)

    def test_hecke_charpolys(self):
        """Test that the Hecke charpolys are correct.

        Some expected Hecke charpolys are stored in the dict test_data,
        which are then checked to be in the relevant page. These examples
        have been chosen to be readily verifiable from the displayed
        Fourier coefficients of each respective homepage."""

        test_data = {# Dimension 1
                    '11/2/a/a' : {2: r'\( 2 + T \)',
                                 17: r'\( 2 + T \)',
                                 29: r'\( T \)'},

                    # Dimension 2
                    '10/3/c/a' :  {5: r'\( 25 + T^{2} \)',
                                  11: r'\( ( 8 + T )^{2} \)',
                                  97: r'\( 7938 + 126 T + T^{2} \)'},

                    # Dimension 5
                    '/294/5/b/f' : {2: r'\( ( 8 + T^{2} )^{5} \)',
                                    # The following test checks that monomials do not have superfluous parentheses
                                    7: r'\( T^{10} \)'},
                    }

        charpoly_test_string = '<td align="left">${}$</td>\n<td>{}</td>'

        for label, some_expected_charpolys in test_data.items():
            page_as_text = self.tc.get('/ModularForm/GL2/Q/holomorphic/{}/'.format(label), follow_redirects=True).get_data(as_text=True)
            for p, expected_pth_charpoly in some_expected_charpolys.items():
                assert charpoly_test_string.format(p, expected_pth_charpoly) in page_as_text

        # Check large dimensions behave as we expect. The following is a form of dimension 108

        large_dimension_page_as_text = self.tc.get('/ModularForm/GL2/Q/holomorphic/671/2/i/a/', follow_redirects=True).get_data(as_text=True)
        assert "Hecke characteristic polynomials" not in large_dimension_page_as_text
