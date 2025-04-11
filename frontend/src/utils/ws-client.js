import { END, eventChannel } from 'redux-saga';

const baseURL = (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.hostname + '/api';

export const createWebSocketConnection = (uri) => {
    return new WebSocket(`${baseURL}${uri}`);
};

export class WebSocketManager {
    constructor() {
        this.ws = null;
    }

    createEventChannel = (uri) => {
        return eventChannel((emit) => {
            const createWs = () => {
                this.ws = createWebSocketConnection(uri);
                this.ws.onmessage = (message) => emit(message.data);
                this.ws.onclose = (e) => {
                    if (e.code === 1005) {
                        emit(END);
                    } else {
                        console.log('Socket is closed Unexpectedly. Reconnect will be attempted in 1 second.', e.code);
                        setTimeout(() => {
                            createWs();
                        }, 1000);
                    }
                };
            }

            createWs();

            return () => {
                this.ws.close();
            };
        });
    }

    wsSend = (message)=> {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(message);
        } else {
            setTimeout(() => {
                this.wsSend(message);
            }, 1000);
        }
    }
}
