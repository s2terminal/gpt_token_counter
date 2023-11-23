from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import tiktoken

@ui.page('/')
def main():
    TOKEN_1K_PRICES = {
        "gpt-4-1106-preview":      { "input": 0.01,   "output": 0.03 },
        "gpt-4":                   { "input": 0.03,   "output": 0.06 },
        "gpt-4-32k":               { "input": 0.06,   "output": 0.12 },
        "gpt-3.5-turbo-1106":      { "input": 0.0010, "output": 0.0020 },
        "gpt-3.5-turbo-instruct":  { "input": 0.0015, "output": 0.0020 },
        "text-embeddings-ada-002": { "input": 0.0001, "output": 0.0001 },
        "ft:gpt-3.5-turbo":        { "input": 0.0030, "output": 0.0060 },
        "ft:davinci-002":          { "input": 0.0120, "output": 0.0120 },
        "ft:babbage-002":          { "input": 0.0016, "output": 0.0016 },
    }
    PRICES_UPDATED_AT = "2023-11-23"

    tokens = { "input": 0, "output": 0 }
    costs = { "us_doller": 0., "jp_yen": 0. }
    params = { "dollar_yen": 150, "model_name": list(TOKEN_1K_PRICES.keys())[0] }

    def count_tokens(input_text: str, model_name: str) -> int:
        encoder = tiktoken.encoding_for_model(model_name)
        encoded = encoder.encode(input_text)
        return len(encoded)

    def token_to_dollar_and_yen(input_token: int, output_token: int, model_name: str) -> tuple[float, float]:
        prices = TOKEN_1K_PRICES[model_name]
        cost_dollar = (input_token * prices["input"] + output_token * prices["output"]) / 1000
        cost_yen = cost_dollar * params["dollar_yen"]
        return (cost_dollar, cost_yen)

    def token_update_handler(_e: ValueChangeEventArguments):
        tokens.update(input=count_tokens(ui_input_text.value, params["model_name"]))
        tokens.update(output=count_tokens(ui_output_text.value, params["model_name"]))
        cost_dollar, cost_yen = token_to_dollar_and_yen(tokens["input"], tokens["output"], params["model_name"])
        costs.update(us_doller=cost_dollar)
        costs.update(jp_yen=cost_yen)

    with ui.grid(columns=2):
        ui_input_text = ui.textarea(placeholder="こんにちは。").on("change", token_update_handler)
        ui_output_text = ui.textarea(placeholder="こんにちは。私は優秀なアシスタントです。どのようにお手伝いできますか？").on("change", token_update_handler)
        ui.label().bind_text_from(tokens, 'input', backward=lambda n: f'input_tokens: {n}')
        ui.label().bind_text_from(tokens, 'output', backward=lambda n: f'output_tokens: {n}')

    with ui.row():
        ui.label().bind_text_from(costs, 'jp_yen', backward=lambda n: f'ざっくり{n:.3f}円').classes("text-xl")

    with ui.column():
        ui.select(list(TOKEN_1K_PRICES.keys()), label="モデル名", on_change=token_update_handler).bind_value(params, 'model_name')
        ui.number(label='ドル円', format='%.2f').bind_value(params, "dollar_yen").on("change", token_update_handler)

        ui.label(f"価格表更新日: {PRICES_UPDATED_AT}")
        ui.link('参考: OpenAI Pricing', 'https://openai.com/pricing')

ui.run()
