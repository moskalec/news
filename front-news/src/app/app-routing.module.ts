import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {NotfoundComponent} from "../shared/components/notfound/notfound.component";
import {AppComponent} from "./app.component";
import {ProfileModule} from "../profile/profile.module";
import {AuthModule} from "../auth/auth.module";

const routes: Routes = [
  {
    path: '', component: AppComponent,
  },
  {
    path: '**', component: NotfoundComponent,
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    AuthModule,
    ProfileModule
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
