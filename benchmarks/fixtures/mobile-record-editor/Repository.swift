struct Repository {
    let api: API
    let cache: DisplayCache

    func load() async throws -> [Item] {
        if let fresh = cache.freshItems() { return fresh }
        let items = try await api.fetchItems()
        cache.replace(items)
        return items
    }

    func update(_ item: Item) async throws {
        try await api.update(item)
        cache.invalidate(item.id)
    }
}
