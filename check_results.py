"""Обобщенные результаты парных прогонов решателя и двух отдельных режимов PINN."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def load(filename):
    return json.loads((DATA / filename).read_text(encoding="utf-8"))


def report_density_profiles():
    print("Давление, Торр | Максимальное расхождение профилей, п. п.")
    for pressure, row in load("density_profiles.json").items():
        selected = [i for i, r in enumerate(row["r_R"]) if 0.2 <= r <= 0.85]
        on = [row["ne_on"][i] for i in selected]
        off = [row["ne_off"][i] for i in selected]
        peak_on, peak_off = max(on), max(off)
        difference = max(abs(a / peak_on - b / peak_off) for a, b in zip(on, off))
        print(f"{pressure:>14} | {100 * difference:.2f}")


def report_held_out_regimes():
    pinn = load("pinn_eval.json")["regimes"]
    control = load("data_only_eval.json")["regimes"]
    print("\nМощность, Вт | Ошибка концентрации, % | PINN, мс | Решатель, ч | Отношение невязок ионизации")
    for key in ("350", "650"):
        row = pinn[key]
        ratio = control[key]["physics_rms"]["ionization"] / row["physics_rms"]["ionization"]
        print(f"{row['P_W']:.0f} | {100 * row['pinn']['ne']:.2f} | "
              f"{1000 * row['pinn_seconds_full_period']:.1f} | "
              f"{row['solver_seconds'] / 3600:.1f} | {ratio:.1f}")


if __name__ == "__main__":
    report_density_profiles()
    report_held_out_regimes()
