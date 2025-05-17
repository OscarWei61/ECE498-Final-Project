import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatRequest {
  task:        string[];    // 跟后端 def generate_full_answer 裡的 task 對應
  input_string: string;     // 跟后端參數名一致
}
export interface ChatResponse {
  formatted_answer: string;              // 后端回傳 { "answer": {...} }
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  // ← 指向你的 Azure VM generate_answer endpoint
  private apiUrl = 'http://20.39.36.144:5100/generate_answer';

  constructor(private http: HttpClient) {}

  sendMessage(
    question: string,
    tasks:    string[]
  ): Observable<ChatResponse> {
    const payload: ChatRequest = {
      task:         tasks,
      input_string: question
    };
    return this.http.post<ChatResponse>(this.apiUrl, payload);
  }
}