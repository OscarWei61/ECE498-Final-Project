import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { MarkdownModule } from 'ngx-markdown';
import { enableProdMode, importProvidersFrom } from '@angular/core';  // ← 把 importProvidersFrom 加进来
// ...

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),           // HttpClient
    importProvidersFrom(MarkdownModule.forRoot()),
    // Other providers...
  ]
}).catch(err => console.error(err));