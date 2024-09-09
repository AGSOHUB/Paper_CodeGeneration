import pandas as pd
from typing import List, Dict, Any, Union
from datetime import datetime
import json
import csv
import gzip
import base64
from cryptography.fernet import Fernet

class DataProcessingFramework:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    # 1. Preprocessing-Interface
    def standardize_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        if isinstance(data, list):
            for item in data:
                if 'date' in item:
                    item['date'] = pd.to_datetime(item['date']).strftime('%Y-%m-%d')
                if 'value' in item:
                    item['value'] = float(item['value'])
        elif isinstance(data, pd.DataFrame):
            if 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
            if 'value' in data.columns:
                data['value'] = data['value'].astype(float)
        return data

    def filter_irrelevant_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        relevant_fields = ['id', 'date', 'value', 'category']
        if isinstance(data, list):
            return [{k: v for k, v in item.items() if k in relevant_fields} for item in data]
        elif isinstance(data, pd.DataFrame):
            return data[relevant_fields]

    def predict_missing_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame], 
                             historical_data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        # This is a simplified implementation. In a real scenario, you'd use more sophisticated prediction methods.
        if isinstance(data, list):
            data = pd.DataFrame(data)
        if isinstance(historical_data, list):
            historical_data = pd.DataFrame(historical_data)
        
        combined_data = pd.concat([historical_data, data]).sort_values('date')
        combined_data['value'] = combined_data['value'].fillna(method='ffill')
        
        return combined_data.tail(len(data))

    # 2. Validation-Interface
    def validate_data_integrity(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> bool:
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        if data['id'].duplicated().any():
            raise ValueError("Duplicate IDs found")
        
        if data['date'].isnull().any() or data['value'].isnull().any():
            raise ValueError("Missing required fields")
        
        return True

    def validate_field_dependencies(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> bool:
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        if not data[data['category'].notnull()]['value'].notnull().all():
            raise ValueError("If category is present, value must also be present")
        
        return True

    def check_value_ranges(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> bool:
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        if (data['value'] < 0).any() or (data['value'] > 1000).any():
            raise ValueError("Values must be between 0 and 1000")
        
        return True

    # 3. Optimization-Interface
    def optimize_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        
        optimized_data = []
        for item in data:
            optimized_item = {k: v for k, v in item.items() if v is not None}
            optimized_data.append(optimized_item)
        
        return optimized_data

    def compress_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> bytes:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        
        json_data = json.dumps(data).encode('utf-8')
        return gzip.compress(json_data)

    def cache_intermediate_results(self, data: Any, key: str):
        # This is a simple in-memory cache. In a real scenario, you might use Redis or another caching solution.
        self.cache = getattr(self, 'cache', {})
        self.cache[key] = data

    # 4. Transformation-Interface
    def convert_data_to_format(self, data: Union[List[Dict[str, Any]], pd.DataFrame], output_format: str) -> str:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        
        if output_format.lower() == 'json':
            return json.dumps(data)
        elif output_format.lower() == 'csv':
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    def encrypt_sensitive_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        sensitive_fields = ['value']
        
        if isinstance(data, pd.DataFrame):
            for field in sensitive_fields:
                if field in data.columns:
                    data[field] = data[field].apply(lambda x: self.cipher_suite.encrypt(str(x).encode()).decode())
        else:
            for item in data:
                for field in sensitive_fields:
                    if field in item:
                        item[field] = self.cipher_suite.encrypt(str(item[field]).encode()).decode()
        
        return data

    def clean_output_data(self, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        fields_to_remove = ['temp_calculation', 'internal_id']
        
        if isinstance(data, pd.DataFrame):
            return data.drop(columns=[f for f in fields_to_remove if f in data.columns])
        else:
            return [{k: v for k, v in item.items() if k not in fields_to_remove} for item in data]

# Example usage
if __name__ == "__main__":
    dpf = DataProcessingFramework()
    
    # Sample data
    sample_data = [
        {"id": 1, "date": "2023-01-01", "value": 100, "category": "A"},
        {"id": 2, "date": "2023-01-02", "value": 200, "category": "B"},
        {"id": 3, "date": "2023-01-03", "value": 300, "category": "C"}
    ]
    
    # Preprocessing
    standardized_data = dpf.standardize_data(sample_data)
    filtered_data = dpf.filter_irrelevant_data(standardized_data)
    
    # Validation
    dpf.validate_data_integrity(filtered_data)
    dpf.validate_field_dependencies(filtered_data)
    dpf.check_value_ranges(filtered_data)
    
    # Optimization
    optimized_data = dpf.optimize_data(filtered_data)
    compressed_data = dpf.compress_data(optimized_data)
    
    # Transformation
    json_output = dpf.convert_data_to_format(optimized_data, 'json')
    encrypted_data = dpf.encrypt_sensitive_data(optimized_data)
    cleaned_data = dpf.clean_output_data(encrypted_data)
    
    print("Processing complete.")