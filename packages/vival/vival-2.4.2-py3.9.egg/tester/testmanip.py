from subprocess import STDOUT, PIPE, CalledProcessError
from collections.abc import Iterable
import subprocess

from distutils.ccompiler import new_compiler

from tester.compiler import Compiler

import os

def scan(text: str, tags: Iterable[str]):
    """Scans given text for every tag from tags. 
    Returns map tag->[positions]"""
    res = {}
    for tag in tags:
        res[tag] = []

        stpos = text.find(tag)
        while (stpos != -1):
            res[tag].append(stpos)

            stpos += len(tag)
            stpos = text.find(tag, stpos)
    
    return res


class Feature:
    """Pair tag->text representing File or Text feature of test"""

    all_tags = { 
        "DESCRIPTION":  { "id": 0, "type": "File", "join_symbol": "\n" },
        "MAIN":         { "id": 1, "type": "File", "join_symbol": "\n" },
        "FLAGS":        { "id": 2, "type": "File", "join_symbol": "\n" },
        "COMMENT":      { "id": 3, "type": "Test", "join_symbol": "\n" },
        "STARTUP":      { "id": 4, "type": "Test", "join_symbol": "\n" },
        "CLEANUP":      { "id": 5, "type": "Test", "join_symbol": "\n" },
        "INPUT":        { "id": 6, "type": "Test", "join_symbol": "\n" },
        "CMD":          { "id": 7, "type": "Test", "join_symbol": " "  },
        "OUTPUT":       { "id": 8, "type": "Test", "join_symbol": "\n" },
    }

    # if not None, will be displayed upon failing a test
    tag_info = { 
        "DESCRIPTION":  None,
        "MAIN":         None,
        "FLAGS":        None,
        "COMMENT":      "",
        "STARTUP":      "ENVIRONMENT PREPARATION",
        "CLEANUP":      None,
        "INPUT":        "INPUT",
        "CMD":          "COMMAND LINE ARGUMENTS",
        "OUTPUT":       "EXPECTED OUTPUT",
    }

    def __init__(self, tag: str, contents: Iterable[str] = None):
        if tag != None:
            self.tag = tag
        else:
            tag = "DESCRIPTION"

        if contents != None:
            self.text = self.all_tags[tag]["join_symbol"].join(contents)
        else:
            self.text = None

    def info(self) -> str:
        """Returns essential info for failed test"""
        return self.tag_info[self.tag]

    def merge_features(self, feature):
        """Pulls text from another feature. 
        Appends if Test feature, replaces otherwise"""
        if self.all_tags[self.tag]["type"] == "Test" and not self.is_empty():
            self.text = self.all_tags[self.tag]["join_symbol"].join(
                [self.text, feature.text]
            )
        else:
            self.text = feature.text

    def is_test_type(self):
        return self.all_tags[self.tag]["type"] == "Test"

    def is_file_type(self):
        return self.all_tags[self.tag]["type"] == "File"

    def is_empty(self):
        return self.text == None

    def __str__(self):
        """Parseable representation of feature"""
        str_repr = ""
        str_repr += self.tag + "\n"

        if self.is_empty():
            str_repr += "/{" + "}/\n\n"
        else:
            str_repr += "/{" + self.text + "}/\n\n"

        return str_repr

    def __repr__(self):
        return str(self)

    def __cmp__(self):
        return self.all_tags[tag]["id"]


def construct_test_features():
    return [
        Feature(tag, None) 
        for tag in Feature.all_tags 
        if Feature.all_tags[tag]["type"] == "Test"
    ]

def construct_file_features():
    return [
        Feature(tag, None) 
        for tag in Feature.all_tags 
        if Feature.all_tags[tag]["type"] == "File"
    ]


class FeatureContainer:
    """Handles storing features"""
    def __init__(self):
        self.features = []

    def add_feature(self, new_feature):
        added_features = {feature.tag : feature for feature in self.features}
        if new_feature.tag in added_features:
            added_features[new_feature.tag].merge_features(new_feature)
        else:
            self.features.append(new_feature)

    def get_feature(self, tag: str):
        return next(
            feature.text 
            for feature in self.features 
            if feature.tag == tag
        )

    def replace_feature(self, new_feature):
        added_features = {feature.tag : feature for feature in self.features}
        if new_feature.tag in added_features:
            added_features[new_feature.tag].text = new_feature.text
        else:
            self.features.append(new_feature)


class Test(FeatureContainer):
    """Single extracted test"""

    def __init__(self, title="Unnamed Test"):
        super(Test, self).__init__()
        self.features = construct_test_features()
        self.title = title
        self.prog_output = None
        self.failed = None

    def run(self, exec_path):
        """Runs executable on this test. Returns True if run succeded"""
        exec_path = os.path.abspath(exec_path)

        cmd = self.get_feature("CMD")
        stdin = self.get_feature("INPUT")
        stdout = self.get_feature("OUTPUT")
        startup = self.get_feature("STARTUP")
        cleanup = self.get_feature("CLEANUP")

        all_args = [exec_path]
        for arg in cmd.split(" "):
            if arg != "":
                all_args.append(arg)

        for args in startup.split("\n"):
            if args != "":
                code = os.waitstatus_to_exitcode(os.system(args))
                if code != 0:
                    self.prog_output = "The program was not executed due to errors during environment preparation stage. Failed to execute: " + args
                    self.failed = True
                    return not self.failed

        prog_output = subprocess.run(all_args, 
                                    stderr=subprocess.STDOUT, 
                                    stdout=PIPE,
                                    input=stdin,
                                    encoding='ascii').stdout
        
        self.prog_output = prog_output

        for args in cleanup.split("\n"):
            if args != "":
                code = os.waitstatus_to_exitcode(os.system(args))
                if code != 0:
                    self.prog_output = "The program was not executed due to errors during environment preparation stage. Failed to execute: " + args
                    self.failed = True
                    return not self.failed

        if self.type == "filled":
            self.failed = (prog_output != stdout)
            return not self.failed
        else:
            self.failed = False
            return not self.failed
    
    def fill(self):
        """Fills in test using last run"""
        self.type = "filled"
        self.replace_feature(Feature("OUTPUT", [self.prog_output]))

    def print_last_run(self):
        """Prints details on last run"""
        print("-" * 30)

        print(self.title)

        for feature in sorted(self.features):
            if not feature.is_empty():
                print(feature)

        print("\nPROGRAM OUTPUT:")
        print(self.prog_output)

        print("-" * 30)

    def __str__(self):
        str_repr = ""

        if self.type == "filled":
            str_repr += self.title + "\n\n"

        if self.type == "unfilled":
            str_repr += self.title + " (unfilled)\n\n"

        for feature in sorted(self.features):
            if not feature.is_empty():
                str_repr += str(feature)
        
        return str_repr

    def add_feature(self, feature):
        super(Test, self).add_feature(feature)

        if feature.tag == "OUTPUT":
            self.type = "filled"
            

class TestsParser(FeatureContainer):
    """Parses text file with tests"""

    def __init__(self, parse_format="new", expected_tests="filled"): 
        super(TestsParser, self).__init__()
        self.features = construct_file_features()
        self.format = parse_format
        self.expected_tests = expected_tests
        self.parse_details = {
            "ntests": 0,
            "format": None,
            "error_message": None,
            "warning_messages": [],
        }

    def parse(self, tests_file):
        """Parses tests_file and returns list of Test objects. Returns None in case of an error"""
        self.parse_details["ntests"] = 0
        tests = []

        text = tests_file.read()

        brackets = scan(text, ["/{", "}/"])

        if len(brackets["/{"]) != len(brackets["}/"]):
            self.parse_details["error_message"] = "Wrong format! Unmatched number of /{ and }/ brackets.\n"
            return None

        if len(brackets["/{"]) == 0 or self.format == "old":
            if self.format == "new":
                self.parse_details["warning_messages"].append("Old format detected!\n")
            return old_parse(text)

        curr_test = Test( "Test " + str(self.parse_details["ntests"] + 1) )
        filled_fields = set()
        prev_tag = None

        section_start = 0
        for lbracket_ind, rbracket_ind in zip(brackets["/{"], brackets["}/"]):
            contents = text[lbracket_ind + len("/{") : rbracket_ind]
            
            wild_space = text[section_start : lbracket_ind]

            # search for tag in wild space
            search_results = scan(wild_space, Feature.all_tags.keys())
            
            best_tag = None
            max_pos = -1
            for tag in search_results:
                if len(search_results[tag]) != 0:
                    curr_max = max(search_results[tag])
                    if curr_max > max_pos:
                        best_tag = tag

                    max_pos = max(curr_max, max_pos)

            if best_tag == None:
                # no tag was found in wild space
                feature = Feature(prev_tag, contents)

                if feature.is_file_type():
                    self.add_feature(feature) 
                
                if feature.is_test_type():
                    curr_test.add_feature(feature)
            else:
                feature = Feature(best_tag, contents)
                if best_tag in filled_fields:
                    # new test has started
                    tests.append(curr_test)

                    self.parse_details["ntests"] += 1
                    curr_test = Test( "Test " + str(self.parse_details["ntests"] + 1) )
                    filled_fields = {best_tag}

                    curr_test.add_feature(feature)
                else:
                    # continue filling in current test
                    if feature.is_file_type():
                        self.add_feature(feature) 
                
                    if feature.is_test_type():
                        filled_fields.add(best_tag)
                        curr_test.add_feature(feature)
                
                prev_tag = best_tag

            section_start = rbracket_ind + len("}/")

        tests.append(curr_test)
        self.parse_details["ntests"] += 1
    
        return tests

    def old_parse(self, text):
        if self.expected_tests == "unfilled":
            contents = list(text.split("[INPUT]\n"))[1:]
            for content in contents:
                curr_test = Test( "Test " + str(self.parse_details["ntests"] + 1) )

                if "{CMD}\n" in content:
                    cmd, inp = content.split("{CMD}\n")

                    curr_test.add_feature(Feature("CMD", cmd))
                else:
                    inp = content

                curr_test.add_feature(Feature("INPUT", inp))

                tests.append(curr_test)
                self.parse_details["ntests"] += 1
        
        if self.expected_tests == "filled":
            contents = list(text.split("[INPUT]\n"))[1:]
            for content in contents:
                curr_test = Test( "Test " + str(self.parse_details["ntests"] + 1) )

                content, outp = content.split("[OUTPUT]\n")

                if "{CMD}\n" in content:
                    cmd, inp = content.split("{CMD}\n")

                    curr_test.add_feature(Feature("CMD", cmd))
                else:
                    inp = content

                curr_test.add_feature(Feature("INPUT", inp))
                curr_test.add_feature(Feature("OUTPUT", outp))

                tests.append(curr_test)
                self.parse_details["ntests"] += 1
                
        return tests

    def write_tests(self, tests, output_filename):
        """Writes contents of tests and parser to output_filename"""
        with open(output_filename, "w") as tsts_file:
            line_len = 70

            tsts_file.write("Contents of this file were automatically generated by VIVAL tool.\n\n")
            tsts_file.write("Install with pip: pip install vival\n")
            tsts_file.write("Visit GitHub for more info: https://github.com/ViktorooReps/vival\n\n")

            for feature in self.features:
                if not feature.is_empty():
                    tsts_file.write(str(feature))

            dashes = (line_len - len("Tests")) // 2
            tsts_file.write(dashes * "-" + "Tests" + dashes * "-" + "\n\n")

            for test in tests:
                tsts_file.write(str(test))
                tsts_file.write("\n\n")

