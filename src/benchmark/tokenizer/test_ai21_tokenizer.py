import pickle
import pytest

from typing import List
from unittest import mock

from common.authentication import Authentication
from common.tokenization_request import TokenizationRequestResult, TokenizationToken, TextRange
from proxy.remote_service import RemoteService
from benchmark.adapter_service import AdapterService
from .tokenizer_factory import TokenizerFactory

TEST_PROMPT: str = (
    "The Center for Research on Foundation Models (CRFM) is "
    "an interdisciplinary initiative born out of the Stanford "
    "Institute for Human-Centered Artificial Intelligence (HAI) "
    "that aims to make fundamental advances in the study, development, "
    "and deployment of foundation models."
)

TEST_TOKEN_REPRESENTATIONS: List[TokenizationToken] = [
    TokenizationToken(value="▁The▁Center▁for", text_range=TextRange(start=0, end=14)),
    TokenizationToken(value="▁Research▁on", text_range=TextRange(start=14, end=26)),
    TokenizationToken(value="▁Foundation", text_range=TextRange(start=26, end=37)),
    TokenizationToken(value="▁Models", text_range=TextRange(start=37, end=44)),
    TokenizationToken(value="▁", text_range=TextRange(start=44, end=45)),
    TokenizationToken(value="(", text_range=TextRange(start=45, end=46)),
    TokenizationToken(value="CRF", text_range=TextRange(start=46, end=49)),
    TokenizationToken(value="M", text_range=TextRange(start=49, end=50)),
    TokenizationToken(value=")", text_range=TextRange(start=50, end=51)),
    TokenizationToken(value="▁is", text_range=TextRange(start=51, end=54)),
    TokenizationToken(value="▁an▁interdisciplinary", text_range=TextRange(start=54, end=75)),
    TokenizationToken(value="▁initiative", text_range=TextRange(start=75, end=86)),
    TokenizationToken(value="▁born▁out▁of", text_range=TextRange(start=86, end=98)),
    TokenizationToken(value="▁the", text_range=TextRange(start=98, end=102)),
    TokenizationToken(value="▁Stanford", text_range=TextRange(start=102, end=111)),
    TokenizationToken(value="▁Institute▁for", text_range=TextRange(start=111, end=125)),
    TokenizationToken(value="▁Human", text_range=TextRange(start=125, end=131)),
    TokenizationToken(value="-Centered", text_range=TextRange(start=131, end=140)),
    TokenizationToken(value="▁Artificial▁Intelligence", text_range=TextRange(start=140, end=164)),
    TokenizationToken(value="▁", text_range=TextRange(start=164, end=165)),
    TokenizationToken(value="(", text_range=TextRange(start=165, end=166)),
    TokenizationToken(value="HAI", text_range=TextRange(start=166, end=169)),
    TokenizationToken(value=")", text_range=TextRange(start=169, end=170)),
    TokenizationToken(value="▁that", text_range=TextRange(start=170, end=175)),
    TokenizationToken(value="▁aims▁to▁make", text_range=TextRange(start=175, end=188)),
    TokenizationToken(value="▁fundamental", text_range=TextRange(start=188, end=200)),
    TokenizationToken(value="▁advances▁in", text_range=TextRange(start=200, end=212)),
    TokenizationToken(value="▁the▁study", text_range=TextRange(start=212, end=222)),
    TokenizationToken(value=",", text_range=TextRange(start=222, end=223)),
    TokenizationToken(value="▁development", text_range=TextRange(start=223, end=235)),
    TokenizationToken(value=",", text_range=TextRange(start=235, end=236)),
    TokenizationToken(value="▁and", text_range=TextRange(start=236, end=240)),
    TokenizationToken(value="▁deployment▁of", text_range=TextRange(start=240, end=254)),
    TokenizationToken(value="▁foundation", text_range=TextRange(start=254, end=265)),
    TokenizationToken(value="▁models", text_range=TextRange(start=265, end=272)),
    TokenizationToken(value=".", text_range=TextRange(start=272, end=273)),
]

TEST_TOKENS: List[str] = [
    "▁The▁Center▁for",
    "▁Research▁on",
    "▁Foundation",
    "▁Models",
    "▁",
    "(",
    "CRF",
    "M",
    ")",
    "▁is",
    "▁an▁interdisciplinary",
    "▁initiative",
    "▁born▁out▁of",
    "▁the",
    "▁Stanford",
    "▁Institute▁for",
    "▁Human",
    "-Centered",
    "▁Artificial▁Intelligence",
    "▁",
    "(",
    "HAI",
    ")",
    "▁that",
    "▁aims▁to▁make",
    "▁fundamental",
    "▁advances▁in",
    "▁the▁study",
    ",",
    "▁development",
    ",",
    "▁and",
    "▁deployment▁of",
    "▁foundation",
    "▁models",
    ".",
]

REQUEST_RESULT: TokenizationRequestResult
LONG_REQUEST_RESULT: TokenizationRequestResult
TRUNCATED_REQUEST_RESULT: TokenizationRequestResult

# The request results are too long to be put here, so we save them to file.
with open("src/benchmark/tokenizer/mock_ai21_tokenizer_request_results.pkl", "rb") as f:
    REQUEST_RESULT, LONG_REQUEST_RESULT, TRUNCATED_REQUEST_RESULT = pickle.load(f)


class TestAI21Tokenizer:
    def setup_method(self):
        # We use mocking for tokenization calls so no valid api_keys are required.
        auth = Authentication(api_key="DUMMY_API_KEY")
        service = AdapterService(RemoteService("DUMMY_URL"), auth)
        self.tokenizer = TokenizerFactory.get_tokenizer("ai21/j1-jumbo", service)

    @mock.patch("benchmark.tokenizer.ai21_tokenizer.TokenizerService.tokenize", return_value=REQUEST_RESULT)
    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_encode(self, mock_tokenize):
        assert self.tokenizer.encode(TEST_PROMPT).tokens == TEST_TOKEN_REPRESENTATIONS

    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_decode(self):
        assert self.tokenizer.decode(TEST_TOKEN_REPRESENTATIONS, TEST_PROMPT) == TEST_PROMPT
        assert self.tokenizer.decode(TEST_TOKEN_REPRESENTATIONS, TEST_PROMPT)[:-1] == TEST_PROMPT[:-1]

    @mock.patch("benchmark.tokenizer.ai21_tokenizer.TokenizerService.tokenize", return_value=REQUEST_RESULT)
    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_tokenize(self, mock_tokenize):
        assert self.tokenizer.tokenize(TEST_PROMPT) == TEST_TOKENS

    @mock.patch("benchmark.tokenizer.ai21_tokenizer.TokenizerService.tokenize", return_value=REQUEST_RESULT)
    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_fits_within_context_window(self, mock_tokenize):
        # Should fit in the context window since we subtracted the number of tokens of the test prompt
        # from the max context window
        assert self.tokenizer.fits_within_context_window(TEST_PROMPT, 2047 - 36)
        # Should not fit in the context window because we're expecting one more extra token in the completion
        assert not self.tokenizer.fits_within_context_window(TEST_PROMPT, 2047 - 36 + 1)

    @mock.patch(
        "benchmark.tokenizer.ai21_tokenizer.TokenizerService.tokenize",
        side_effect=[LONG_REQUEST_RESULT, LONG_REQUEST_RESULT, TRUNCATED_REQUEST_RESULT, TRUNCATED_REQUEST_RESULT],
    )
    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_truncate_from_right(self, mock_tokenize):
        # Create a prompt that exceed max context length: 36 * 57 = 2052 tokens.
        # Our naive concatenation of the strings here also leads to extra tokens.
        long_prompt: str = TEST_PROMPT * 57
        assert not self.tokenizer.fits_within_context_window(long_prompt)

        # Truncate and ensure it fits within the context window
        truncated_long_prompt: str = self.tokenizer.truncate_from_right(long_prompt)
        assert self.tokenizer.tokenize_and_count(truncated_long_prompt) == 2047
        assert self.tokenizer.fits_within_context_window(truncated_long_prompt)

    @mock.patch("benchmark.tokenizer.ai21_tokenizer.TokenizerService.tokenize", return_value=REQUEST_RESULT)
    @pytest.mark.skip("TODO: update the pickle file with the response")
    def test_tokenize_and_count(self, mock_tokenize):
        assert self.tokenizer.tokenize_and_count(TEST_PROMPT) == 36
