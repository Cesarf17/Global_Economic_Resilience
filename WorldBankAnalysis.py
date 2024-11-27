import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TourismImpactAnalysis:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)
        self.top_tourism_countries = [
            'France', 'Spain', 'United States', 'China', 
            'Italy', 'Turkey', 'Mexico', 'Thailand',
            'Germany', 'United Kingdom'
        ]
        
    def preprocess_data(self):
        tourism_data = {}
        
        # Manual data for missing values
        tourism_values = {
            'France': {'2019': 65.0e9, '2020': 32.0e9},
            'Spain': {'2019': 71.2e9, '2020': 27.0e9},
            'United States': {'2019': 193.3e9, '2020': 76.1e9},
            'China': {'2019': 45.0e9, '2020': 35.0e9},
            'Italy': {'2019': 49.6e9, '2020': 20.0e9},
            'Turkey': {'2019': 29.8e9, '2020': 12.1e9},
            'Mexico': {'2019': 24.6e9, '2020': 10.2e9},
            'Thailand': {'2019': 60.5e9, '2020': 15.0e9},
            'Germany': {'2019': 58.0e9, '2020': 40.0e9},
            'United Kingdom': {'2019': 52.7e9, '2020': 21.0e9}
        }
        
        for country in self.top_tourism_countries:
            country_data = {}
            
            # Get GDP data for both years
            gdp_data = self.data[
                (self.data['Country Name'] == country) &
                (self.data['Indicator Code'] == 'NY.GDP.PCAP.CD')
            ]
            
            if not gdp_data.empty:
                try:
                    country_data['GDP_2019'] = gdp_data['2019'].values[0]
                    country_data['GDP_2020'] = gdp_data['2020'].values[0]
                    country_data['GDP_Change'] = ((country_data['GDP_2020'] - country_data['GDP_2019']) / 
                                               country_data['GDP_2019'] * 100)
                except:
                    print(f"Missing GDP data for {country}")
                    continue
            
            # Use manual tourism data
            if country in tourism_values:
                country_data['Tourism_2019'] = tourism_values[country]['2019']
                country_data['Tourism_2020'] = tourism_values[country]['2020']
                country_data['Tourism_Change'] = ((country_data['Tourism_2020'] - country_data['Tourism_2019']) / 
                                               country_data['Tourism_2019'] * 100)
            
                try:
                    country_data['Tourism_GDP_Ratio_2019'] = (country_data['Tourism_2019'] / 
                                                        (country_data['GDP_2019'] * 1e6)) * 100
                    country_data['Tourism_GDP_Ratio_2020'] = (country_data['Tourism_2020'] / 
                                                        (country_data['GDP_2020'] * 1e6)) * 100
                except:
                    print(f"Error calculating ratios for {country}")
                    continue
            
            tourism_data[country] = country_data
        
        return pd.DataFrame.from_dict(tourism_data, orient='index')

    def plot_tourism_receipts_comparison(self, df):
        plt.figure(figsize=(12, 6))
        x = np.arange(len(df.index))
        width = 0.35
        
        plt.bar(x - width/2, df['Tourism_2019']/1e9, width, label='2019', color='#2ecc71')
        plt.bar(x + width/2, df['Tourism_2020']/1e9, width, label='2020', color='#e74c3c')
        
        plt.ylabel('Tourism Receipts (Billion USD)', fontsize=12)
        plt.title('Tourism Receipts Comparison (2019 vs 2020)', fontsize=14, pad=20)
        plt.xticks(x, df.index, rotation=45)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add value labels
        for i, v in enumerate(df['Tourism_2019']/1e9):
            plt.text(i - width/2, v, f'{v:.1f}', ha='center', va='bottom')
        for i, v in enumerate(df['Tourism_2020']/1e9):
            plt.text(i + width/2, v, f'{v:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('tourism_receipts_comparison.png', bbox_inches='tight', dpi=300)
        plt.show()

    def plot_percentage_changes(self, df):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Tourism Change
        df_sorted = df.sort_values('Tourism_Change')
        bars1 = ax1.barh(df_sorted.index, df_sorted['Tourism_Change'],
                        color=['#e74c3c' if x < 0 else '#2ecc71' for x in df_sorted['Tourism_Change']])
        ax1.set_xlabel('Percentage Change (%)', fontsize=12)
        ax1.set_title('Tourism Receipts Change (2019-2020)', fontsize=14, pad=20)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Add value labels
        for i, v in enumerate(df_sorted['Tourism_Change']):
            ax1.text(v, i, f'{v:.1f}%', ha='left' if v < 0 else 'right', va='center')
        
        # GDP Change
        df_sorted = df.sort_values('GDP_Change')
        bars2 = ax2.barh(df_sorted.index, df_sorted['GDP_Change'],
                        color=['#e74c3c' if x < 0 else '#2ecc71' for x in df_sorted['GDP_Change']])
        ax2.set_xlabel('Percentage Change (%)', fontsize=12)
        ax2.set_title('GDP Change (2019-2020)', fontsize=14, pad=20)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Add value labels
        for i, v in enumerate(df_sorted['GDP_Change']):
            ax2.text(v, i, f'{v:.1f}%', ha='left' if v < 0 else 'right', va='center')
        
        plt.tight_layout()
        plt.savefig('percentage_changes.png', bbox_inches='tight', dpi=300)
        plt.show()

    def plot_tourism_gdp_contribution(self, df):
        plt.figure(figsize=(12, 6))
        x = np.arange(len(df.index))
        width = 0.35
        
        plt.bar(x - width/2, df['Tourism_GDP_Ratio_2019'], width, 
                label='2019', color='#2ecc71')
        plt.bar(x + width/2, df['Tourism_GDP_Ratio_2020'], width, 
                label='2020', color='#e74c3c')
        
        # Add value labels
        for i, v in enumerate(df['Tourism_GDP_Ratio_2019']):
            plt.text(i - width/2, v, f'{v:.1f}%', ha='center', va='bottom')
        for i, v in enumerate(df['Tourism_GDP_Ratio_2020']):
            plt.text(i + width/2, v, f'{v:.1f}%', ha='center', va='bottom')
        
        plt.ylabel('Tourism Receipts as % of GDP', fontsize=12)
        plt.title('Tourism Contribution to GDP (2019 vs 2020)', fontsize=14, pad=20)
        plt.xticks(x, df.index, rotation=45)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('tourism_gdp_contribution.png', bbox_inches='tight', dpi=300)
        plt.show()

def main():
    analysis = TourismImpactAnalysis('WDICSV.csv')
    analyzed_data = analysis.preprocess_data()
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("\nAverage Tourism Change: {:.2f}%".format(analyzed_data['Tourism_Change'].mean()))
    print("Average GDP Change: {:.2f}%".format(analyzed_data['GDP_Change'].mean()))
    print("\nCountry with largest tourism decline: {} ({:.2f}%)".format(
        analyzed_data['Tourism_Change'].idxmin(),
        analyzed_data['Tourism_Change'].min()
    ))
    print("Country with smallest tourism decline: {} ({:.2f}%)".format(
        analyzed_data['Tourism_Change'].idxmax(),
        analyzed_data['Tourism_Change'].max()
    ))
    
    # Display plots one after another
    print("\nDisplaying Tourism Receipts Comparison...")
    analysis.plot_tourism_receipts_comparison(analyzed_data)
    
    input("\nPress Enter to see Percentage Changes comparison...")
    analysis.plot_percentage_changes(analyzed_data)
    
    input("\nPress Enter to see Tourism Contribution to GDP...")
    analysis.plot_tourism_gdp_contribution(analyzed_data)

if __name__ == "__main__":
    main()