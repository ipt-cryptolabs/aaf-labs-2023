#pragma once

#include <unordered_map>
#include <string>

#include "Trie.h"

class CommandProcessor
{
public:
    void start();

    static CommandProcessor* get()
    {
        static CommandProcessor processor;
        return &processor;
    }

    void create(const std::string& set_name);
    void print_tree(const std::string& set_name);
    void insert(const std::string& set_name, const std::string& value);
    void contains(const std::string& set_name, const std::string& value);
    void search(const std::string& set_name, const std::string& search_type = Tokens::ASC);
    void between(const std::string& set_name, const std::string& from, const std::string& to, 
                    const std::string& order = Tokens::ASC);
    void match(const std::string& set_name, const std::string& pattern, const std::string& order = Tokens::ASC);
    
private:
    explicit CommandProcessor() = default;
    CommandProcessor(const CommandProcessor& processor) = delete;
    CommandProcessor& operator=(const CommandProcessor& processor) = delete;
    ~CommandProcessor() = default;

private:
    std::unordered_map<std::string, Trie> m_tries;
};