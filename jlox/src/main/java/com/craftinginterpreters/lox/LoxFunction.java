package com.craftinginterpreters.lox;

import java.util.List;

class LoxFunction implements LoxCallable {

    private final Environment closure;
    private final Stmt.Function declaration;
    private final boolean isInitializer;

    LoxFunction(
        Stmt.Function declaration,
        Environment closure,
        boolean isInitializer
    ) {
        this.isInitializer = isInitializer;
        this.closure = closure;
        this.declaration = declaration;
    }

    public LoxFunction bind(LoxInstance instance) {
        Environment environment = new Environment(closure);
        environment.define("this", instance);
        return new LoxFunction(declaration, environment, this.isInitializer);
    }

    @Override
    public Object call(Interpreter interpreter, List<Object> arguments) {
        Environment environment = new Environment(closure);
        for (int i = 0; i < declaration.params.size(); i++) {
            environment.define(
                declaration.params.get(i).lexeme,
                arguments.get(i)
            );
        }

        try {
            interpreter.executeBlock(declaration.body, environment);
        } catch (Return returnValue) {
            if (this.isInitializer) {
                return closure.getAt(0, "this");
            }
            return returnValue.value;
        }

        // If you directly call `init` on an object, return the object itself.
        if (isInitializer) return closure.getAt(0, "this");

        return null;
    }

    @Override
    public int arity() {
        return declaration.params.size();
    }

    @Override
    public String toString() {
        return "<fn " + declaration.name.lexeme + ">";
    }
}
