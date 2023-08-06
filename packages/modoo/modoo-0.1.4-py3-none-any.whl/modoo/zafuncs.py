# built-ins
from functools import reduce
from operator import itemgetter
from copy import deepcopy
import re


def merge_docs(za_s_docs, za_o_docs):
    def by_id_reducer(acc, doc):
        _id = doc['id']
        acc[_id] = doc
        return acc

    def merge_reducer(acc, doc):
        _id = doc['id']
        za_s = doc['ZA']
        za_o = acc[_id]['ZA']
        acc[_id]['ZA'] = [*za_s, *za_o]
        return acc
    za_o_docs_by_id = reduce(by_id_reducer, deepcopy(za_o_docs), {})
    return [*reduce(merge_reducer, za_s_docs, za_o_docs_by_id).values()]


def fold_docs(docs):
    def fold_zas(zas):
        def reducer(acc, za):
            pred = za['predicate']
            snt_id, begin, end = itemgetter(
                'sentence_id', 'begin', 'end')(pred)
            key = f'{snt_id}-{begin}-{end}'

            if key in acc:
                acc[key]['antecedent'] = [
                    *acc[key]['antecedent'],
                    *za['antecedent']
                ]
            else:
                acc[key] = za

            return acc
        return reduce(reducer, zas, {}).values()

    def sort_zas(zas):
        def parse_snt_id(snt_id):
            p_order, snt_order = re.match(
                r'.+?(\d+?)\.(\d+?)$', snt_id).groups()
            return dict(p_order=int(p_order), snt_order=int(snt_order))

        def sort_by_p_order(za):
            return parse_snt_id(za['predicate']['sentence_id'])['p_order']

        def sort_by_snt_order(za):
            return parse_snt_id(za['predicate']['sentence_id'])['snt_order']

        def sort_by_begin(za):
            return za['predicate']['begin']

        sorted_by_begin = sorted(zas, key=sort_by_begin)
        sorted_by_snt_order = sorted(sorted_by_begin, key=sort_by_snt_order)
        return sorted(sorted_by_snt_order, key=sort_by_p_order)

    def fold_doc(doc):
        zas = doc['ZA']
        return {**doc, 'ZA': sort_zas(fold_zas(zas))}

    return [*map(fold_doc, docs)]


def compare_num_za(za_s_docs, za_o_docs, za_so_docs, za_docs):
    def mapper(elem):
        _id, za = itemgetter('id', 'ZA')(elem)
        return [_id, len(za)]

    za_s_check = map(mapper, za_s_docs)
    za_o_check = map(mapper, za_o_docs)
    za_so_check = map(mapper, za_so_docs)
    za_check = map(mapper, za_docs)

    def by_id_reducer(acc, curr):
        _id = curr[0]
        acc[_id] = curr
        return acc

    def append_reducer(acc, curr):
        _id, num_za = curr
        acc[_id] = [*acc[_id], num_za]
        return acc

    za_s_hash = reduce(by_id_reducer, za_s_check, {})
    za_o_hash = reduce(append_reducer, za_o_check, za_s_hash)
    za_so_hash = reduce(append_reducer, za_so_check, za_o_hash)
    za_hash = reduce(append_reducer, za_check, za_so_hash)
    header = ['id', 'num_za_s', 'num_za_o', 'num_za_s+o', 'num_za_merged']
    return [header, *za_hash.values()]
