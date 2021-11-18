from datetime import date, datetime
import unittest

from CamlQueryBuilder.camlQueryBuilder import CamlOperatorType, CamlFilter, CamlWhere, CamlAnd, CamlOr

class Test_gen(unittest.TestCase):

    def test_int(self):
        m_filter = CamlFilter(CamlOperatorType.Equal, 'Somme', 2)
        query_text = CamlWhere(m_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Somme" /><Value Type="Integer">2</Value></Eq></Where>')

    def test_float(self):
        m_filter = CamlFilter(CamlOperatorType.Equal, 'Somme', 2.3)
        query_text = CamlWhere(m_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Somme" /><Value Type="Number">2.3</Value></Eq></Where>')

    def test_text(self):
        m_filter = CamlFilter(CamlOperatorType.Equal, 'Title', 'book')
        query_text = CamlWhere(m_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Title" /><Value Type="Text">book</Value></Eq></Where>')

    def test_bool(self):
        m_filter = CamlFilter(CamlOperatorType.Equal, 'valided', True)
        query_text = CamlWhere(m_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="valided" /><Value Type="Integer">1</Value></Eq></Where>')

    def test_date(self):
        date_filter = CamlFilter(CamlOperatorType.Equal, 'Created', date(2021,11,17))
        query_text = CamlWhere(date_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Created" /><Value IncludeTimeValue="FALSE" Type="DateTime">2021-11-17</Value></Eq></Where>')
    
    def test_dateTime(self):
        date_filter = CamlFilter(CamlOperatorType.Equal, 'Created', datetime(2021,11,17,20,43,33))
        query_text = CamlWhere(date_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Created" /><Value IncludeTimeValue="TRUE" Type="DateTime">2021-11-17T20:43:33</Value></Eq></Where>')

    def test_inList(self):
        somme_filter = CamlFilter(CamlOperatorType.InList, 'Somme', 10, 11, 12)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><In><FieldRef Name="Somme" /><Values><Value Type="Integer">10</Value><Value Type="Integer">11</Value><Value Type="Integer">12</Value></Values></In></Where>')

    def test_isNull(self):
        somme_filter = CamlFilter(CamlOperatorType.IsNull, 'Somme')
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><IsNull><FieldRef Name="Somme" /></IsNull></Where>')

    def test_isNotNull(self):
        somme_filter = CamlFilter(CamlOperatorType.IsNotNull, 'Somme')
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><IsNotNull><FieldRef Name="Somme" /></IsNotNull></Where>')

    def test_equal(self):
        somme_filter = CamlFilter(CamlOperatorType.Equal, 'Somme', 10)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><Eq><FieldRef Name="Somme" /><Value Type="Integer">10</Value></Eq></Where>')

    def test_lower_or_equal(self):
        somme_filter = CamlFilter(CamlOperatorType.LowerOrEqual, 'Somme', 10)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><Leq><FieldRef Name="Somme" /><Value Type="Integer">10</Value></Leq></Where>')

    def test_different(self):
        somme_filter = CamlFilter(CamlOperatorType.Different, 'Somme', 10)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><Neq><FieldRef Name="Somme" /><Value Type="Integer">10</Value></Neq></Where>')

    def test_lower(self):
        somme_filter = CamlFilter(CamlOperatorType.Lower, 'Somme', 10)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><Lt><FieldRef Name="Somme" /><Value Type="Integer">10</Value></Lt></Where>')

    def test_lower_or_equal(self):
        somme_filter = CamlFilter(CamlOperatorType.LowerOrEqual, 'Somme', 10)
        query_text = CamlWhere(somme_filter).query_text
        self.assertEqual(query_text, '<Where><Leq><FieldRef Name="Somme" /><Value Type="Integer">10</Value></Leq></Where>')

    def test_beginsWith(self):
        title_filter = CamlFilter(CamlOperatorType.BeginsWith, 'Title', 'm')
        query_text = CamlWhere(title_filter).query_text
        self.assertEqual(query_text, '<Where><BeginsWith><FieldRef Name="Title" /><Value Type="Text">m</Value></BeginsWith></Where>')

    def test_contains(self):
        title_filter = CamlFilter(CamlOperatorType.Contains, 'Title', 'm')
        query_text = CamlWhere(title_filter).query_text
        self.assertEqual(query_text, '<Where><Contains><FieldRef Name="Title" /><Value Type="Text">m</Value></Contains></Where>')

    def test_orderBy(self):
        title_filter = CamlFilter(CamlOperatorType.Contains, 'Title', 'book')
        query_text = CamlWhere(title_filter).orderBy('Created').query_text
        self.assertEqual(query_text, '<Where><Contains><FieldRef Name="Title" /><Value Type="Text">book</Value></Contains></Where><OrderBy><FieldRef Name="Created" Ascending="True" /></OrderBy>')
    
    def test_and(self):
        filter_1 = CamlFilter(CamlOperatorType.Different, 'Title', 'My book')
        filter_2 = CamlFilter(CamlOperatorType.LowerOrEqual, 'Price', 200)
        query_text = CamlWhere(CamlAnd(filter_1, filter_2)).query_text
        self.assertEqual(query_text, '<Where><And><Neq><FieldRef Name="Title" /><Value Type="Text">My book</Value></Neq><Leq><FieldRef Name="Price" /><Value Type="Integer">200</Value></Leq></And></Where>')
    
    def test_or(self):
        filter_1 = CamlFilter(CamlOperatorType.Different, 'Title', 'My book')
        filter_2 = CamlFilter(CamlOperatorType.LowerOrEqual, 'Price', 200)
        query_text = CamlWhere(CamlOr(filter_1, filter_2)).query_text
        self.assertEqual(query_text, '<Where><Or><Neq><FieldRef Name="Title" /><Value Type="Text">My book</Value></Neq><Leq><FieldRef Name="Price" /><Value Type="Integer">200</Value></Leq></Or></Where>')

    def test_and_or(self):
        filter_1 = CamlFilter(CamlOperatorType.Different, 'Title', 'My book')
        filter_2 = CamlFilter(CamlOperatorType.LowerOrEqual, 'Price', 200)
        filter_3 = CamlFilter(CamlOperatorType.BeginsWith, 'Author', 'Georges')
        query_text = CamlWhere(CamlAnd(CamlOr(filter_1, filter_3), filter_2)).query_text
        self.assertEqual(query_text, '<Where><And><Or><Neq><FieldRef Name="Title" /><Value Type="Text">My book</Value></Neq><BeginsWith><FieldRef Name="Author" /><Value Type="Text">Georges</Value></BeginsWith></Or><Leq><FieldRef Name="Price" /><Value Type="Integer">200</Value></Leq></And></Where>')

        query_text = CamlWhere(CamlOr(CamlAnd(filter_1, filter_3), filter_2)).query_text
        self.assertEqual(query_text, '<Where><Or><And><Neq><FieldRef Name="Title" /><Value Type="Text">My book</Value></Neq><BeginsWith><FieldRef Name="Author" /><Value Type="Text">Georges</Value></BeginsWith></And><Leq><FieldRef Name="Price" /><Value Type="Integer">200</Value></Leq></Or></Where>')

if __name__ == '__main__':
    unittest.main()