// test.ts

// Basic types
const message: string = "TypeScript is working!";
const num: number = 42;
const isActive: boolean = true;

// Function with types
function greet(name: string): string {
    return `Hello, ${name}!`;
}

// Arrow function
const add = (a: number, b: number): number => a + b;

// Interface
interface User {
    id: number;
    name: string;
}

// Object using interface
const user: User = {
    id: 1,
    name: "Garry"
};

// Test output
console.log(message);
console.log("Number:", num);
console.log("Active:", isActive);
console.log(greet(user.name));
console.log("Add result:", add(5, 3));

// Intentional type check (uncomment to test compiler error)
// const bad: number = "this should fail";