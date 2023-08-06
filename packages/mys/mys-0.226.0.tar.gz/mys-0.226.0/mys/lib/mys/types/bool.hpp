#pragma once

namespace mys {

// To make str(bool) and print(bool) show True and False.
struct Bool {
    bool m_value;

    Bool() : m_value(false)
    {
    }

    Bool(bool value) : m_value(value)
    {
    }

    operator bool() const
    {
        return m_value;
    }
};

std::ostream& operator<<(std::ostream& os, const Bool& obj);

}

namespace std
{
    template<> struct hash<mys::Bool>
    {
        std::size_t operator()(mys::Bool const& s) const noexcept
        {
            return s.m_value;
        }
    };
}
