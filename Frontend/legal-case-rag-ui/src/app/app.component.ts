// src/app/app.component.ts
import { Component } from '@angular/core';
import { ChatComponent } from './components/chat/chat.component';

@Component({
  selector: 'app-root',
  standalone: true,      // ← standalone
  imports: [ChatComponent],
  template: `<app-chat></app-chat>`
})
export class AppComponent {}