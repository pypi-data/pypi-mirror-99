#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple test queries [for DEVELOPMENT  / not part of official tests]

$ pip instal -e .
$ dimcli_quicktest 1

"""

import click 
import os
import requests

from .. import *
from ..utils import *
from ..core.converters import *

from ..utils.gists_utils import *



@click.command()
@click.argument('test_number', nargs=1)
def main(test_number=1):
    
    login()
    dsl = Dsl()
    test_number = int(test_number)

    if test_number == 1:

        covid_q = '"2019-nCoV" OR "COVID-19" OR "SARS-CoV-2" OR (("coronavirus"  OR "corona virus") AND (Wuhan OR China))'
        q = f"""search publications 
                in full_data for "{dsl_escape(covid_q)}" 
                where year=2020 
            return publications[id+doi+pmid+pmcid+title+journal+publisher+mesh_terms+date+year+volume+issue+pages+open_access_categories+type+authors+research_orgs+funders+supporting_grant_ids+times_cited+altmetric+linkout] limit 1000"""

        q1 = """search publications for "malaria" return publications[id+authors]"""

        click.secho(q, fg="green")

        df = dslquery(q).as_dataframe()

        r = DfConverter(df, "publications")
        res = r.simplify_nested_objects()

        order = [   'Publication ID', 
                    'DOI',
                    'PMID',
                    'PMCID',
                    'Title',
                    'Abstract',
                    'Source title',
                    'Source UID',
                    'Publisher',
                    'MeSH terms',
                    'Publication Date',
                    'PubYear',
                    'Volume',
                    'Issue',
                    'Pagination',
                    'Open Access',
                    'Publication Type',
                    'Authors',
                    'Corresponding Author',
                    'Authors Affiliations',
                    'Research Organizations - standardized',
                    'GRID IDs',
                    'City of Research organization',
                    'Country of Research organization',
                    'Funder',
                    'UIDs of supporting grants',
                    'Times cited',
                    'Altmetric',
                    'Source Linkout',
                    'Dimensions URL']

        res = res[order]

        res.to_csv("test.csv", index=False)

    if test_number == 2:
        from dimcli.functions import extract_affiliations
        bad_data=[{'name': 'Universidad Central de Bayamon',
        'city': 'Bayamón',
        'state': 'Puerto Rico',
        'country': 'United States'}]
        print(extract_affiliations(bad_data))

    if test_number == 3:
        from dimcli.utils.repl_utils import export_gist
        q = "search publications return category_for limit 100"
        data = dsl.query(q)
        export_gist(data.json, q, dsl._url)


if __name__ == '__main__':
    main()



