import { Component }    from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule }  from '@angular/forms';
import { ChatService }  from '../../services/chat.service';
import { MarkdownModule } from 'ngx-markdown';
interface Message {
  content: string;
  sender:  'user' | 'bot';
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [ CommonModule, FormsModule, MarkdownModule ],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent {
  messages: Message[] = [];
  userInput = '';
  loading   = false;

  isLegalSearch      = false;
  isSimilarRetrieval = false;

  // ↓↓↓ 新增這兩行 ↓↓↓
  states = [
    'Illinois','Alabama','Alaska','Arizona','Arkansas','California','Colorado',
    'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Indiana',
    'Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts',
    'Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska',
    'Nevada','New Hampshire','New Jersey','New Mexico','New York',
    'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania',
    'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
    'Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'
  ];
  selectedState = this.states[0];

  constructor(private chatService: ChatService) {}

  sendMessage(): void {
    const text = this.userInput.trim();
    if (!text) return;

    const tasks = ['general_answer'];
    if (this.isLegalSearch)      tasks.push('legal_statute_search');
    if (this.isSimilarRetrieval) tasks.push('similar_case_retrieval');

    this.messages.push({ content: text, sender: 'user' });
    this.userInput = '';
    this.loading   = true;

    this.chatService.sendMessage(text, tasks).subscribe({
      next: res => {
        // 直接讀 formatted_answer
        const reply = res.formatted_answer;
        this.messages.push({ content: reply, sender: 'bot' });
        this.loading = false;
      },
      error: () => {
        this.messages.push({ content: 'Error: unable to reach backend.', sender: 'bot' });
        this.loading = false;
      }
    });
  }
}