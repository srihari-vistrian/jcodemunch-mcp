"""Tests for language-specific parsing."""

import pytest
from jcodemunch_mcp.parser import parse_file


JAVASCRIPT_SOURCE = '''
/** Greet a user. */
function greet(name) {
    return `Hello, ${name}!`;
}

class Calculator {
    /** Add two numbers. */
    add(a, b) {
        return a + b;
    }
}

const MAX_RETRY = 5;
'''


def test_parse_javascript():
    """Test JavaScript parsing."""
    symbols = parse_file(JAVASCRIPT_SOURCE, "app.js", "javascript")
    
    # Should have function, class, method, constant
    func = next((s for s in symbols if s.name == "greet"), None)
    assert func is not None
    assert func.kind == "function"
    assert "Greet a user" in func.docstring
    
    cls = next((s for s in symbols if s.name == "Calculator"), None)
    assert cls is not None
    assert cls.kind == "class"
    
    method = next((s for s in symbols if s.name == "add"), None)
    assert method is not None
    assert method.kind == "method"


TYPESCRIPT_SOURCE = '''
interface User {
    name: string;
}

/** Get user by ID. */
function getUser(id: number): User {
    return { name: "Test" };
}

class UserService {
    private users: User[] = [];
    
    @cache()
    findById(id: number): User | undefined {
        return this.users.find(u => u.id === id);
    }
}

type ID = string | number;
'''


def test_parse_typescript():
    """Test TypeScript parsing."""
    symbols = parse_file(TYPESCRIPT_SOURCE, "service.ts", "typescript")
    
    # Should have interface, function, class, method, type alias
    func = next((s for s in symbols if s.name == "getUser"), None)
    assert func is not None
    assert func.kind == "function"
    
    interface = next((s for s in symbols if s.name == "User"), None)
    assert interface is not None
    assert interface.kind == "type"


GO_SOURCE = '''
package main

import "fmt"

// Person represents a person.
type Person struct {
    Name string
}

// Greet prints a greeting.
func (p *Person) Greet() {
    fmt.Println("Hello, " + p.Name)
}

// Add adds two numbers.
func Add(a, b int) int {
    return a + b
}

const MaxCount = 100
'''


def test_parse_go():
    """Test Go parsing."""
    symbols = parse_file(GO_SOURCE, "main.go", "go")
    
    # Should have type, method, function, constant
    person = next((s for s in symbols if s.name == "Person"), None)
    assert person is not None
    assert person.kind == "type"
    
    greet = next((s for s in symbols if s.name == "Greet"), None)
    assert greet is not None
    assert greet.kind == "method"


RUST_SOURCE = '''
/// A user in the system.
pub struct User {
    name: String,
}

impl User {
    /// Create a new user.
    pub fn new(name: &str) -> Self {
        Self { name: name.to_string() }
    }
    
    /// Get the user's name.
    pub fn name(&self) -> &str {
        &self.name
    }
}

pub const MAX_USERS: usize = 1000;
'''


def test_parse_rust():
    """Test Rust parsing."""
    symbols = parse_file(RUST_SOURCE, "user.rs", "rust")
    
    # Should have struct, impl, methods, constant
    user = next((s for s in symbols if s.name == "User"), None)
    assert user is not None
    assert user.kind == "type"


JAVA_SOURCE = '''
/**
 * A simple calculator.
 */
public class Calculator {
    public static final int MAX_VALUE = 100;
    
    /**
     * Add two numbers.
     */
    public int add(int a, int b) {
        return a + b;
    }
}

interface Operable {
    int operate(int a, int b);
}
'''


def test_parse_java():
    """Test Java parsing."""
    symbols = parse_file(JAVA_SOURCE, "Calculator.java", "java")

    # Should have class, method, interface
    calc = next((s for s in symbols if s.name == "Calculator"), None)
    assert calc is not None
    assert calc.kind == "class"

    add = next((s for s in symbols if s.name == "add"), None)
    assert add is not None
    assert add.kind == "method"


PHP_SOURCE = '''<?php

const MAX_RETRIES = 3;

/**
 * Authenticate a user token.
 */
function authenticate(string $token): bool
{
    return strlen($token) > 0;
}

/**
 * Manages user operations.
 */
class UserService
{
    /**
     * Get a user by ID.
     */
    public function getUser(int $userId): array
    {
        return ['id' => $userId];
    }
}

interface Authenticatable
{
    public function authenticate(string $token): bool;
}

trait Timestampable
{
    public function getCreatedAt(): string
    {
        return date(\'Y-m-d\');
    }
}

enum Status
{
    case Active;
    case Inactive;
}
'''


def test_parse_php():
    """Test PHP parsing."""
    symbols = parse_file(PHP_SOURCE, "service.php", "php")

    func = next((s for s in symbols if s.name == "authenticate"), None)
    assert func is not None
    assert func.kind == "function"
    assert "Authenticate a user token" in func.docstring

    cls = next((s for s in symbols if s.name == "UserService"), None)
    assert cls is not None
    assert cls.kind == "class"

    method = next((s for s in symbols if s.name == "getUser"), None)
    assert method is not None
    assert method.kind == "method"
    assert "Get a user by ID" in method.docstring

    interface = next((s for s in symbols if s.name == "Authenticatable"), None)
    assert interface is not None
    assert interface.kind == "type"

    trait = next((s for s in symbols if s.name == "Timestampable"), None)
    assert trait is not None
    assert trait.kind == "type"

    enum = next((s for s in symbols if s.name == "Status"), None)
    assert enum is not None
    assert enum.kind == "type"


C_SOURCE = '''
// A person struct
struct Person {
    char* name;
    int age;
};

union Data {
    int i;
    float f;
};

enum Color { RED, GREEN, BLUE };

typedef unsigned long size_t;

typedef void (*callback_t)(int, int);

// Add two numbers
int add(int a, int b) {
    return a + b;
}

// Get name
char* get_name(void) {
    return "hello";
}
'''


def test_parse_c():
    """Test C parsing."""
    symbols = parse_file(C_SOURCE, "main.c", "c")

    func = next((s for s in symbols if s.name == "add"), None)
    assert func is not None
    assert func.kind == "function"
    assert "Add two numbers" in func.docstring

    # Pointer-return function name extracted correctly
    ptr_func = next((s for s in symbols if s.name == "get_name"), None)
    assert ptr_func is not None
    assert ptr_func.kind == "function"

    struct = next((s for s in symbols if s.name == "Person"), None)
    assert struct is not None
    assert struct.kind == "type"

    union = next((s for s in symbols if s.name == "Data"), None)
    assert union is not None
    assert union.kind == "type"

    enum = next((s for s in symbols if s.name == "Color"), None)
    assert enum is not None
    assert enum.kind == "type"

    typedef = next((s for s in symbols if s.name == "size_t"), None)
    assert typedef is not None
    assert typedef.kind == "type"

    # Function pointer typedef name extracted without parens/asterisk
    fn_ptr = next((s for s in symbols if s.name == "callback_t"), None)
    assert fn_ptr is not None
    assert fn_ptr.kind == "type"


CPP_SOURCE = '''
// A vector utility class
class Vector {
public:
    // Constructor
    Vector(double x, double y) : x_(x), y_(y) {}

    // Get magnitude
    double magnitude() const {
        return 0.0;
    }

private:
    double x_;
    double y_;
};

struct Point {
    double x;
    double y;
};

union Data {
    int i;
    float f;
};

enum class Direction { North, South, East, West };

namespace math {
    // Compute factorial
    int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
}

template<typename T>
T max_val(T a, T b) {
    return a > b ? a : b;
}

template<typename T>
class Container {
public:
    void add(T item) {}
};

using IntAlias = int;

// Add two numbers
int add(int a, int b) {
    return a + b;
}
'''


def test_parse_cpp():
    """Test C++ parsing."""
    symbols = parse_file(CPP_SOURCE, "main.cpp", "cpp")

    cls = next((s for s in symbols if s.name == "Vector"), None)
    assert cls is not None
    assert cls.kind == "class"

    method = next((s for s in symbols if s.name == "magnitude"), None)
    assert method is not None
    assert method.kind == "method"

    # Constructor
    ctor = next((s for s in symbols if s.qualified_name == "Vector.Vector"), None)
    assert ctor is not None
    assert ctor.kind == "method"

    struct = next((s for s in symbols if s.name == "Point"), None)
    assert struct is not None
    assert struct.kind == "type"

    union = next((s for s in symbols if s.name == "Data"), None)
    assert union is not None
    assert union.kind == "type"

    enum = next((s for s in symbols if s.name == "Direction"), None)
    assert enum is not None
    assert enum.kind == "type"

    ns = next((s for s in symbols if s.name == "math"), None)
    assert ns is not None
    assert ns.kind == "type"

    # Template function
    tmpl_func = next((s for s in symbols if s.name == "max_val"), None)
    assert tmpl_func is not None
    assert tmpl_func.kind == "function"

    # Template class
    tmpl_cls = next((s for s in symbols if s.name == "Container"), None)
    assert tmpl_cls is not None
    assert tmpl_cls.kind == "class"

    # Using alias
    alias = next((s for s in symbols if s.name == "IntAlias"), None)
    assert alias is not None
    assert alias.kind == "type"

    func = next((s for s in symbols if s.name == "add" and s.kind == "function"), None)
    assert func is not None
    assert "Add two numbers" in func.docstring

