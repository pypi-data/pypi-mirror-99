import pytest

from sym.sdk.errors import InvalidSRNError, SRNTrailingSeparatorError
from sym.sdk.resource import SRN


class TestResource:
    def test_sym_resource_fails_on_malformed_srn(self):
        bad_1 = "foo"
        bad_2 = "foo:bar"
        bad_3 = "foo:bar:baz"
        bad_4 = "foo:bar:baz:boz"
        bad_5 = "foo:bar:baz:lates:"
        bad_6 = "foo:bar:baz:1.0:"
        bad_7 = "foo:bar:baz:1.0.0::"
        bad_8 = "foo:bar:baz:latest:1.0.0:"
        bad_9 = "foo:bar:baz:1.3000.0:something"
        bad_10 = "foo:bar:baz::something"
        bad_11 = "foo:bar:baz:latestsomething"
        bad_12 = "foo:bar:baz:latest:"  # Good except for trailing separator
        bad_13 = "foo_foobar:bar:baz:latest:foo"  # Has underscore
        bad_14 = "sym:flow:something::"
        bad_15 = "foo_foobar:bar:baz:1000.0.2000:foo"  # Has two bad parts

        self._test_bad(bad_1, InvalidSRNError)
        self._test_bad(bad_2, InvalidSRNError)
        self._test_bad(bad_3, InvalidSRNError)
        self._test_bad(bad_4, InvalidSRNError)
        msg_5 = f"SRN {bad_5} is not valid because it has a trailing separator."
        self._test_bad(bad_5, SRNTrailingSeparatorError, match=msg_5)
        self._test_bad(bad_6, InvalidSRNError)
        self._test_bad(bad_7, InvalidSRNError)
        self._test_bad(bad_8, SRNTrailingSeparatorError)
        self._test_bad(bad_9, InvalidSRNError)
        self._test_bad(bad_10, InvalidSRNError)
        self._test_bad(bad_11, InvalidSRNError)
        self._test_bad(bad_12, InvalidSRNError)
        msg_13 = f"SRN {bad_13} is not valid. The invalid parts were: [org]."
        self._test_bad(bad_13, InvalidSRNError)
        self._test_bad(bad_14, InvalidSRNError)
        msg_15 = f"SRN {bad_15} is not valid. The invalid parts were: [org, version]."
        self._test_bad(bad_15, InvalidSRNError)

    def _test_bad(self, srn, exc, match: str = None):
        if match:
            with pytest.raises(exc, match=match):
                SRN.from_string(srn)
        else:
            with pytest.raises(exc):
                SRN.from_string(srn)

    def test_sym_srn_succeeds_on_valid_srn(self):
        good_1 = "sym:foo-bar:12345-11233:0.1.0:stuff"
        good_2 = "foo:bar:baz:1.300.0:something"  # Max of 3 digits in semver
        good_3 = "foo:bar:baz:latest"
        good_4 = "sym:template:approval:1.0.0"
        good_5 = "sym:template:approval:1.0.0:e97af6b3-0249-4855-971f-4e1dd188773a"

        self._test_good(good_1)
        self._test_good(good_2)
        self._test_good(good_3)
        self._test_good(good_4)
        self._test_good(good_5)

    def _test_good(self, raw):
        SRN.from_string(raw)
        SRN.parse(raw)  # Will raise if the SRN is bad

    def test_srn_copy_should_succeed_without_identifier(self):
        srn_string = "foo:bar:baz:1.0.0"

        srn = SRN.from_string(srn_string)

        assert str(srn.copy(version="latest")) == "foo:bar:baz:latest"
        assert str(srn.copy(organization="myorg")) == "myorg:bar:baz:1.0.0"

    def test_srn_str_should_produce_an_identical_srn(self):
        text = "sym:template:approval:1.0.0"
        srn = SRN.from_string(text)

        srn_str = str(srn)
        srn2 = SRN.from_string(srn_str)

        assert srn == srn2
        assert str(srn) == str(srn2)
        assert text == srn_str
