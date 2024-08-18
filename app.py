import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Load the saved Ridge Regression model
model = joblib.load('ridge_model.pkl')

# Function to make predictions
def predict(features):
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0]  # Return as scalar

# Function to create a plotly graph
def create_graph(user_input, prediction):
    categories = [
        "ROA(C)", "Gross Margin", "Profit Rate", "Interest Rate",
        "Expense Rate", "R&D Expense", "Cash Flow", "Debt Interest",
        "Net Value", "Current Ratio"
    ]

    fig = go.Figure()

    # Add bar chart for input features
    fig.add_trace(go.Bar(
        x=categories,
        y=user_input,
        name='User Input',
        marker_color='indigo'
    ))

    # Add prediction result as a line
    fig.add_trace(go.Scatter(
        x=categories,
        y=[prediction] * len(categories),
        mode='lines+markers',
        name='Prediction',
        line=dict(color='firebrick', width=4)
    ))

    fig.update_layout(
        title='Financial Performance Prediction',
        xaxis_title='Features',
        yaxis_title='Values',
        barmode='group',
        plot_bgcolor='white'
    )

    return fig

# Function to display prediction form and results
def display_prediction_form():
    st.title("Predict Financial Performance")
    
    # Input fields for each feature with unique keys
    roa = st.number_input("Enter value for ROA(C) before interest and depreciation before interest", value=0.0, key="roa")
    gross_margin = st.number_input("Enter value for Operating Gross Margin", value=0.0, key="gross_margin")
    profit_rate = st.number_input("Enter value for Operating Profit Rate", value=0.0, key="profit_rate")
    interest_rate = st.number_input("Enter value for Pre-tax net Interest Rate", value=0.0, key="interest_rate")
    expense_rate = st.number_input("Enter value for Operating Expense Rate", value=0.0, key="expense_rate")
    r_d_expense = st.number_input("Enter value for Research and development expense rate", value=0.0, key="r_d_expense")
    cash_flow = st.number_input("Enter value for Cash flow rate", value=0.0, key="cash_flow")
    debt_interest = st.number_input("Enter value for Interest-bearing debt interest rate", value=0.0, key="debt_interest")
    net_value = st.number_input("Enter value for Net Value Per Share (B)", value=0.0, key="net_value")
    current_ratio = st.number_input("Enter value for Current Ratio", value=0.0, key="current_ratio")

    # Collect user input
    user_input = [
        roa, gross_margin, profit_rate, interest_rate, expense_rate,
        r_d_expense, cash_flow, debt_interest, net_value, current_ratio
    ]

    # When the user clicks the predict button
    if st.button("Predict"):
        prediction = predict(user_input)
        # Convert prediction to a scalar if it is a numpy array
        if isinstance(prediction, np.ndarray):
            prediction = prediction.item()

        # Display the prediction output with explanation
        st.markdown(
            f"<h2 style='color:darkblue;'>Net Income to Stockholders Equity: {prediction * 100:.2f}%</h2>"
            f"<p style='font-size:16px;'>This indicates that for every dollar of stockholders' equity, "
            f"the company generates {prediction * 100:.2f}% in net income.</p>",
            unsafe_allow_html=True
        )

        # Display the graph and prediction output side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_graph(user_input, prediction))

        with col2:
            st.markdown(
                f"<h2 style='color:darkblue;'>Net Income to Stockholders Equity: {prediction * 100:.2f}%</h2>"
                f"<p style='font-size:16px;'>This indicates that for every dollar of stockholders' equity, "
                f"the company generates {prediction * 100:.2f}% in net income.</p>",
                unsafe_allow_html=True
            )

        # Add a "Back" button to return to the home page
        if st.button("Back to Home"):
            st.session_state.active_section = None

# Function to display stats and graphs
def display_stats():
    st.title("Financial Performance Stats")
    st.write("This section will display various statistics and graphs related to financial performance.")
    # Here you can include stats and graphs
    st.write("Add your stats and graphs here.")
    # Add a "Back" button to return to the home page
    if st.button("Back to Home"):
        st.session_state.active_section = None

# Streamlit app main function
def main():
    st.markdown("<h1 style='text-align: center; color: black;'>Financial Performance Dashboard</h1>", unsafe_allow_html=True)

    # Ensure the state of which section is active is maintained
    if "active_section" not in st.session_state:
        st.session_state.active_section = None

    if st.session_state.active_section is None:
        # Display the main action buttons
        st.markdown(
            """
            <style>
            .button-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 50px;
            }
            .stButton button {
                background-color: #007bff;
                color: white;
                padding: 20px 40px;
                border: none;
                border-radius: 10px;
                font-size: 22px;
                font-weight: bold;
                transition: background-color 0.3s, transform 0.3s;
                margin: 10px;
                width: 300px;
            }
            .stButton button:hover {
                background-color: #0056b3;
                transform: translateY(-2px);
            }
            .stButton button:active {
                background-color: #004494;
                transform: translateY(1px);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            if st.button("Predict Financial Performance"):
                st.session_state.active_section = "predict"
        with col2:
            if st.button("Display Stats"):
                st.session_state.active_section = "stats"

    # Handle navigation logic
    if st.session_state.active_section == "predict":
        display_prediction_form()
    elif st.session_state.active_section == "stats":
        display_stats()

if __name__ == "__main__":
    main()
