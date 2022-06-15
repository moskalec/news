import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {AuthLayoutComponent} from "./layout/auth-layout/auth-layout.component";
import {RegistrationComponent} from "./components/registration/registration.component";

const routes: Routes = [
  {
    path: '', component: AuthLayoutComponent, children: [
      {
        path: 'login', component: LoginComponent
      },

      {
        path: 'registration', component: RegistrationComponent
      }
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
