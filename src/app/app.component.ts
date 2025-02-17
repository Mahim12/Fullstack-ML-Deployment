import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';  // ✅ Required for ngModel!
import { NgIf, NgFor, CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,  
  imports: [IonicModule, HttpClientModule, FormsModule, NgIf, NgFor, CommonModule],  // ✅ Ensure FormsModule is here
  templateUrl: './app.component.html'
})
export class AppComponent {
  features: { name: string; value: number }[] = [
    { name: 'CRIM (Per capita crime rate)', value: 0 },
    { name: 'ZN (Residential land proportion)', value: 0 },
    { name: 'INDUS (Non-retail business acres per town)', value: 0 },
    { name: 'CHAS (Charles River dummy variable)', value: 0 },
    { name: 'NOX (Nitric oxide concentration)', value: 0 },
    { name: 'RM (Avg. number of rooms per dwelling)', value: 0 },
    { name: 'AGE (Proportion of old owner-occupied units)', value: 0 },
    { name: 'DIS (Weighted distance to employment centers)', value: 0 },
    { name: 'RAD (Index of accessibility to highways)', value: 0 },
    { name: 'TAX (Property-tax rate per $10,000)', value: 0 },
    { name: 'PTRATIO (Pupil-teacher ratio by town)', value: 0 },
    { name: 'B (1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town)', value: 0 },
    { name: 'LSTAT (% lower status population)', value: 0 }
  ];
  
  predictedPrice: number | null = null;
  loading: boolean = false;
  
  constructor(private http: HttpClient) {}
  
  predictHousePrice() {
    const apiUrl = 'http://127.0.0.1:5000/predict'; // Change if hosted online
    const inputValues = this.features.map(feature => feature.value);
  
    this.loading = true;
    this.http.post<{ predicted_price: number }>(apiUrl, { features: inputValues }).subscribe(
      response => {
        this.predictedPrice = response.predicted_price;
        this.loading = false;
      },
      error => {
        console.error('Error:', error);
        this.loading = false;
      }
    );
  }
}
