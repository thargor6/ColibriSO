
// intermediate solution from the official Vaadin CRM Demo
import { login as loginImpl, logout as logoutImpl } from '@vaadin/flow-frontend';
import type { LoginResult } from '@vaadin/flow-frontend';
import * as UserEndpoint from './generated/UserEndpoint';
import {Store} from "./store";

const LAST_LOGIN_TIMESTAMP = 'lastLoginTimestamp';
const SESSION_USER_ID = 'sessionUserId';
const THIRTY_DAYS_MS = 6 * 60 * 60 * 1000;
const lastLoginTimestamp = localStorage.getItem(LAST_LOGIN_TIMESTAMP);
const hasRecentLoginTimestamp = (lastLoginTimestamp &&
  (new Date().getTime() - new Date(+lastLoginTimestamp).getTime()) < THIRTY_DAYS_MS) || false;

let _isLoggedIn = hasRecentLoginTimestamp;

export async function login(username: string, password: string): Promise<LoginResult> {
  if (_isLoggedIn) {
    return { error: false } as LoginResult;
  } else {
    const result = await loginImpl(username, password);
    if (!result.error) {
      await postLogin(username);
      _isLoggedIn = true;
      localStorage.setItem(LAST_LOGIN_TIMESTAMP, new Date().getTime() + '')
    }
    return result;
  }
}

async function postLogin(username: string) {
  const user = await UserEndpoint.getByUsername(username);
  localStorage.setItem(SESSION_USER_ID, user?.id);
  Store.getInstance().clearSessionData();
  await Store.getInstance().init();
}

export async function logout() {
  _isLoggedIn = false;
  localStorage.removeItem(LAST_LOGIN_TIMESTAMP);
  localStorage.removeItem(SESSION_USER_ID);
  Store.getInstance().clearSessionData();
  return await logoutImpl();
}

export function isLoggedIn() {
  return _isLoggedIn;
}

export function setSessionExpired() {
  _isLoggedIn = false;
  localStorage.removeItem(LAST_LOGIN_TIMESTAMP);
}

export function getSessionUserId() {
  return localStorage.getItem(SESSION_USER_ID);
}