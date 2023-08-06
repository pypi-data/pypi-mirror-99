import os
from quicktions import Fraction
from itertools import permutations
from unittest import TestCase

from musicscore.basic_functions import flatten
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


def _generate_test_32_groups():
    def _permute_without_duplicates(input_list):
        return [list(x) for x in list(dict.fromkeys(list(permutations(input_list))))]

    output = {
        1: [[1, 1, 1, 1, 1, 1, 1, 1]],
        2: _permute_without_duplicates([2, 1, 1, 1, 1, 1, 1]),
        3: _permute_without_duplicates([2, 2, 1, 1, 1, 1]),
        4: _permute_without_duplicates([2, 2, 3, 1]),
        5: _permute_without_duplicates([2, 3, 1, 1, 1]),
        6: _permute_without_duplicates([2, 4, 1, 1]),
        7: _permute_without_duplicates([2, 5, 1]),
        8: _permute_without_duplicates([3, 1, 1, 1, 1, 1]),
        9: _permute_without_duplicates([3, 3, 1, 1]),
        10: _permute_without_duplicates([3, 4, 1]),
        11: _permute_without_duplicates([4, 1, 1, 1, 1]),
        12: _permute_without_duplicates([5, 1, 1, 1]),
        13: _permute_without_duplicates([6, 1, 1]),
        14: _permute_without_duplicates([7, 1]),
        15: _permute_without_duplicates([3, 3, 2]),

    }

    return output


THIRTY_SECOND_GROUPS = _generate_test_32_groups()


def convert_32_groups_to_quarter_durations(groups):
    return [[x / 8 for x in group] for group in groups]


def get_32_groups(keys):
    output = []
    for key in keys:
        output.extend(THIRTY_SECOND_GROUPS[key])
    return output


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()
        self.score.page_style.format = 'portrait'

    def test_1(self):
        sf = SimpleFormat(quarter_durations=(1.5, 0.5, 1.5))
        v = sf.to_stream_voice(1)
        self.score.set_time_signatures(times={1: (7, 8)})
        v.add_to_score(self.score)
        xml_path = path + '_test_1.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=(0.25, 0.25))
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        xml_path = path + '_test_2.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_3(self):
        sf = SimpleFormat(quarter_durations=(0.25, 0.125, 0.125, 0.25, 0.25))
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)
        xml_path = path + '_test_3.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    def test_iter_permutations(self):
        input_list = [1, 2, 3]
        actual = list(permutations(input_list))
        expected = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
        self.assertEqual(expected, actual)

    def test_iter_permutations_duplicates(self):
        input_list = [1, 1, 2]
        actual = list(dict.fromkeys(list(permutations(input_list))))
        expected = [(1, 1, 2), (1, 2, 1), (2, 1, 1)]
        self.assertEqual(expected, actual)

    def test_32_groups(self):
        actual = _generate_test_32_groups()
        expected = {1: [[1, 1, 1, 1, 1, 1, 1, 1]],
                    2: [[2, 1, 1, 1, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 1],
                        [1, 1, 2, 1, 1, 1, 1],
                        [1, 1, 1, 2, 1, 1, 1],
                        [1, 1, 1, 1, 2, 1, 1],
                        [1, 1, 1, 1, 1, 2, 1],
                        [1, 1, 1, 1, 1, 1, 2]],
                    3: [[2, 2, 1, 1, 1, 1],
                        [2, 1, 2, 1, 1, 1],
                        [2, 1, 1, 2, 1, 1],
                        [2, 1, 1, 1, 2, 1],
                        [2, 1, 1, 1, 1, 2],
                        [1, 2, 2, 1, 1, 1],
                        [1, 2, 1, 2, 1, 1],
                        [1, 2, 1, 1, 2, 1],
                        [1, 2, 1, 1, 1, 2],
                        [1, 1, 2, 2, 1, 1],
                        [1, 1, 2, 1, 2, 1],
                        [1, 1, 2, 1, 1, 2],
                        [1, 1, 1, 2, 2, 1],
                        [1, 1, 1, 2, 1, 2],
                        [1, 1, 1, 1, 2, 2]],
                    4: [[2, 2, 3, 1],
                        [2, 2, 1, 3],
                        [2, 3, 2, 1],
                        [2, 3, 1, 2],
                        [2, 1, 2, 3],
                        [2, 1, 3, 2],
                        [3, 2, 2, 1],
                        [3, 2, 1, 2],
                        [3, 1, 2, 2],
                        [1, 2, 2, 3],
                        [1, 2, 3, 2],
                        [1, 3, 2, 2]],
                    5: [[2, 3, 1, 1, 1],
                        [2, 1, 3, 1, 1],
                        [2, 1, 1, 3, 1],
                        [2, 1, 1, 1, 3],
                        [3, 2, 1, 1, 1],
                        [3, 1, 2, 1, 1],
                        [3, 1, 1, 2, 1],
                        [3, 1, 1, 1, 2],
                        [1, 2, 3, 1, 1],
                        [1, 2, 1, 3, 1],
                        [1, 2, 1, 1, 3],
                        [1, 3, 2, 1, 1],
                        [1, 3, 1, 2, 1],
                        [1, 3, 1, 1, 2],
                        [1, 1, 2, 3, 1],
                        [1, 1, 2, 1, 3],
                        [1, 1, 3, 2, 1],
                        [1, 1, 3, 1, 2],
                        [1, 1, 1, 2, 3],
                        [1, 1, 1, 3, 2]],
                    6: [[2, 4, 1, 1],
                        [2, 1, 4, 1],
                        [2, 1, 1, 4],
                        [4, 2, 1, 1],
                        [4, 1, 2, 1],
                        [4, 1, 1, 2],
                        [1, 2, 4, 1],
                        [1, 2, 1, 4],
                        [1, 4, 2, 1],
                        [1, 4, 1, 2],
                        [1, 1, 2, 4],
                        [1, 1, 4, 2]],
                    7: [[2, 5, 1], [2, 1, 5], [5, 2, 1], [5, 1, 2], [1, 2, 5], [1, 5, 2]],
                    8: [[3, 1, 1, 1, 1, 1],
                        [1, 3, 1, 1, 1, 1],
                        [1, 1, 3, 1, 1, 1],
                        [1, 1, 1, 3, 1, 1],
                        [1, 1, 1, 1, 3, 1],
                        [1, 1, 1, 1, 1, 3]],
                    9: [[3, 3, 1, 1],
                        [3, 1, 3, 1],
                        [3, 1, 1, 3],
                        [1, 3, 3, 1],
                        [1, 3, 1, 3],
                        [1, 1, 3, 3]],
                    10: [[3, 4, 1], [3, 1, 4], [4, 3, 1], [4, 1, 3], [1, 3, 4], [1, 4, 3]],
                    11: [[4, 1, 1, 1, 1],
                         [1, 4, 1, 1, 1],
                         [1, 1, 4, 1, 1],
                         [1, 1, 1, 4, 1],
                         [1, 1, 1, 1, 4]],
                    12: [[5, 1, 1, 1], [1, 5, 1, 1], [1, 1, 5, 1], [1, 1, 1, 5]],
                    13: [[6, 1, 1], [1, 6, 1], [1, 1, 6]],
                    14: [[7, 1], [1, 7]],
                    15: [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
                    }
        self.assertEqual(expected, actual)

    def test_get_32_groups(self):
        keys = [1, 2]
        actual = get_32_groups(keys)
        expected = [[1, 1, 1, 1, 1, 1, 1, 1],
                    [2, 1, 1, 1, 1, 1, 1],
                    [1, 2, 1, 1, 1, 1, 1],
                    [1, 1, 2, 1, 1, 1, 1],
                    [1, 1, 1, 2, 1, 1, 1],
                    [1, 1, 1, 1, 2, 1, 1],
                    [1, 1, 1, 1, 1, 2, 1],
                    [1, 1, 1, 1, 1, 1, 2]]
        self.assertEqual(expected, actual)

    def test_convert_groups(self):
        keys = [1, 2]
        actual = convert_32_groups_to_quarter_durations(get_32_groups(keys))
        expected = [[0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
                    [0.25, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
                    [0.125, 0.25, 0.125, 0.125, 0.125, 0.125, 0.125],
                    [0.125, 0.125, 0.25, 0.125, 0.125, 0.125, 0.125],
                    [0.125, 0.125, 0.125, 0.25, 0.125, 0.125, 0.125],
                    [0.125, 0.125, 0.125, 0.125, 0.25, 0.125, 0.125],
                    [0.125, 0.125, 0.125, 0.125, 0.125, 0.25, 0.125],
                    [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.25]]
        self.assertEqual(expected, actual)

    def test_set_break_beam(self):
        sf = SimpleFormat(quarter_durations=[4])
        sf.to_stream_voice().add_to_score(self.score)
        self.score.break_beam_32 = True
        actual = self.score.break_beam_32
        self.assertTrue(actual)
        part = self.score.get_measure(1).get_part(1)
        actual = part.break_beam_32
        self.assertTrue(actual)
        actual = self.score.get_measure(1).get_part(1).tree_part_staves[1].tree_part_voices[1].break_beam_32
        self.assertTrue(actual)

    def test_32_first_group(self):
        self.score.set_time_signatures(times={1: (1, 4)})
        self.score.break_beam_32 = True
        keys = [1]
        all_durations = flatten(convert_32_groups_to_quarter_durations(get_32_groups(keys)))
        sf = SimpleFormat(quarter_durations=all_durations)

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_32_first_group.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_all_possible_32s(self):
        self.score.break_beam_32 = True
        self.score.set_time_signatures(times={1: (1, 4)})
        keys = list(range(1, 16))
        all_durations = flatten(convert_32_groups_to_quarter_durations(get_32_groups(keys)))
        sf = SimpleFormat(quarter_durations=all_durations)

        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_all_possible_32s.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_beam_break_with_quantization(self):
        quarter_durations = [Fraction(2, 1), Fraction(1, 1), Fraction(3, 2), Fraction(5, 2), Fraction(1, 1),
                             Fraction(2, 1), Fraction(3, 1), Fraction(1, 1), Fraction(3, 2), Fraction(1, 2),
                             Fraction(4, 15), Fraction(2, 5), Fraction(1, 3), Fraction(8, 15), Fraction(8, 45),
                             Fraction(2, 9), Fraction(4, 15), Fraction(16, 75), Fraction(8, 25), Fraction(4, 15),
                             Fraction(3, 5), Fraction(1, 2), Fraction(2, 5), Fraction(1, 2), Fraction(1, 3),
                             Fraction(2, 5), Fraction(4, 15), Fraction(16, 75), Fraction(4, 15), Fraction(8, 25),
                             Fraction(8, 15), Fraction(2, 3)]

        self.score.break_beam_32 = True
        self.score.forbidden_divisions = [5, 6, 7]
        sf = SimpleFormat(quarter_durations=quarter_durations)
        sf.to_stream_voice().add_to_score(self.score)
        xml_path = path + '_beam_break_with_quantization.xml'
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
