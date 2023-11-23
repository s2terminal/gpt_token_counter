from nicegui import ui

@ui.page('/')
def main():
    tokens = { "num": 0 }
    OUTPUT_1K_DOLLAR = 0.03
    DOLLAR_YEN = 150

    def count_tokens(input_text: str) -> int:
        # TODO: tiktokenで数える
        return len(input_text)

    def token_to_dollar_and_yen(token_num: int) -> tuple[float, float]:
        cost_dollar = token_num * OUTPUT_1K_DOLLAR / 1000
        cost_yen = cost_dollar * DOLLAR_YEN
        return (cost_dollar, cost_yen)

    def handle_cost(token_num: int) -> str:
        cost_dollar, cost_yen = token_to_dollar_and_yen(token_num)
        return f'${cost_dollar:.3f} ({cost_yen:.3f}円)'

    ui.textarea('入力してね').bind_value_to(tokens, 'num', forward=lambda t: count_tokens(t))

    ui.label().bind_text_from(tokens, 'num', backward=lambda n: f'tokens: {n}')
    ui.label().bind_text_from(tokens, 'num', backward=lambda n: handle_cost(n))

    ui.label(f"OUTPUT_1K_DOLLAR: {OUTPUT_1K_DOLLAR}")
    ui.label(f"DOLLAR_YEN: {DOLLAR_YEN}")


    ui.link('参考: OpenAI Pricing', 'https://openai.com/pricing')


ui.run()
