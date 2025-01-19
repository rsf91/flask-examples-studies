from flask import Flask, render_template, request
import numpy as np
# import matplotlib.pyplot as plt
# from sabr import sabr_volatility

import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

import matplotlib.pyplot as plt

import sabr_methods



app = Flask(__name__)

# Função para calcular o smile de volatilidade
def calculate_vol_smile(alpha, beta, rho, volvol, f0, strikes):
    volatilities = np.array([1,2,3]) # [sabr_volatility(f0, k, 1.0, alpha, beta, rho, volvol) for k in strikes]
    volatilities = np.linspace(50, 150, 50) * np.random.rand()
    return volatilities

@app.route("/", methods=["GET", "POST"])
def index():
    vol_smile = None
    strikes = np.linspace(50, 150, 50)  # Exemplo de strikes para o cálculo
    
    if request.method == "POST":
        try:
            alpha = float(request.form["alpha"])
            beta = float(request.form["beta"])
            rho = float(request.form["rho"])
            volvol = float(request.form["volvol"])
            f0 = float(request.form["f0"])
            t_expire = float(request.form["t_expire"])

            print(f0) # até aqui funciona
            
            # vol_smile = calculate_vol_smile(alpha, beta, rho, volvol, f0, strikes)

            strikes = np.linspace(80, 120, 10)
            vol_smile = sabr_methods.sabr_smile(f0, t_expire, alpha, beta, rho, volvol, strikes)

            print(vol_smile)
            print(strikes)

            # Gerar o gráfico
            plt.figure(figsize=(8, 5))
            plt.plot(strikes, vol_smile, label="Volatility Smile")
            plt.xlabel("Strike Price")
            plt.ylabel("Implied Volatility")
            plt.title("SABR Model Volatility Smile")
            plt.legend()
            plt.grid()
            plt.savefig("static/vol_smile.png")
            plt.close()
        except ValueError:
            print(f"Error occurred: {e}")
            vol_smile = None  # Ensure it remains defined
            return "Por favor, insira valores válidos."


    return render_template("index.html", vol_smile=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)
