import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProfileRoutingModule } from './profile-routing.module';
import { DashboardComponent } from './components/dashboard/dashboard.component';

import { MatSliderModule } from '@angular/material/slider';


@NgModule({
  declarations: [
    DashboardComponent
  ],
  imports: [
    CommonModule,
    ProfileRoutingModule,
    MatSliderModule,
  ]
})
export class ProfileModule { }
