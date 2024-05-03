import '@testing-library/jest-dom';
global.console = {
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn(),
    info: jest.fn(),
    debug: jest.fn(),
  };
global.URL.createObjectURL = jest.fn(() => "http://mocked.url/object");